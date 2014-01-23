import json
import math
import os
from string import lower
import zipfile
import re
import urllib
import random
import csv
import time

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.utils.translation import ugettext as _, get_language
from registration.backends.default.views import RegistrationView

from vpw.models import Material, Author, Settings
from vpw.utils import normalize_string
from vpw.vpr_api import vpr_get_material, vpr_get_category, vpr_get_person, \
    vpr_get_categories, vpr_browse, vpr_materials_by_author, vpr_get_pdf, vpr_search, vpr_delete_person, vpr_get_statistic_data, \
    voer_get_attachment_info, vpr_create_material, vpr_get_material_images, voer_update_author, voer_add_favorite, vpr_search_author, vpr_search_module, \
    voer_add_view_count, vpr_get_content_file, vpr_get_user_avatar, vpr_get_favorite
from vpw.vpr_api import vpt_import, vpt_get_url, vpt_download, vpr_request
from vpw.forms import ModuleCreationForm, EditProfileForm, CollectionCreationForm, SettingsForm, RecaptchaRegistrationForm



# Template for create module
MODULE_TEMPLATES = [
    '',
    'frontend/module/create_step1.html',
    'frontend/module/create_step2.html',
    'frontend/module/create_step3.html',
]

# Template for create collection
COLLECTION_TEMPLATES = [
    '',
    'frontend/collection/create_step1.html',
    'frontend/collection/create_step2.html',
    'frontend/collection/create_step3.html',
]

# Material type
MODULE_TYPE = 1
COLLECTION_TYPE = 2

EXPORT_PDF_DIR = '%s/pdf_export/' % settings.MEDIA_ROOT


class RecaptchaRegistrationView(RegistrationView):
    """
    Subclass of RegistrationView that uses RecaptchaRegistrationForm
    """
    form_class = RecaptchaRegistrationForm


# Create your views here.
def home(request):
    # material_features = ['64b4a7a7', 'fd2f579c', 'f2feed3c', '4dbdd6c5', 'c3ad3533', '0e60bfc6']
    material_features_sample = ['01f46fc2', '022e4f84', '0e60bfc6', '2d2e6a46', '3ec080b8', '45df218a', '4c212f92',
                                '4dbdd6c5', 'b14d14a4', 'c3ad3533', 'd4aa7723', 'f2feed3c', 'fd2f579c']
    material_features = random.sample(material_features_sample, 6)
    materials_list = []
    for mid in material_features:
        material = vpr_get_material(mid)
        if 'material_id' not in material:
            continue
        author_id_list = material['author'].split(',')

        p_list = []
        for pid in author_id_list:
            pid = pid.strip()
            person = vpr_get_person(pid)
            if person['fullname']:
                p_list.append({'pid': pid, 'pname': person['fullname']})
            else:
                p_list.append({'pid': pid, 'pname': person['fullname']})
        material['author_list'] = p_list
        materials_list.append(material)

    # Get featured authors
    person_features = [50, 214, 702, 1651, 69]
    person_list = []
    for pid in person_features:
        person = vpr_get_person(pid)
        if 'id' in person:
            person_list.append(person)

    return render(request, "frontend/index.html",
                  {"materials_list": materials_list, "person_list": person_list, "is_home": True})


def signup(request):
    return render(request, "frontend/signup.html")


def aboutus(request):
    return render(request, "frontend/aboutus.html")


def _get_image(list_images):
    def replace_image(match_object):
        try:
            result = "<img src='" + list_images[match_object.group(1)] + "'"
        except KeyError:
            result = "<img src='" + match_object.group(1) + "'"
        return result

    return replace_image


def module_detail(request, title, mid, version):
    material = vpr_get_material(mid)
    # lay anh trong noi dung
    list_images = vpr_get_material_images(mid)
    # content = re.sub(r'<img[^>]*src="([^"]*)"', _get_image(list_images), material['text'])
    content = re.sub(r'<img[^>]*src="([^"]*)"', _get_image(list_images), material['text'])
    material['text'] = content

    author = []
    if 'author' in material and material['author']:
        author_id_list = material['author'].split(',')

        for pid in author_id_list:
            pid = pid.strip()
            person = vpr_get_person(pid, True)
            if person:
                author.append(person)

    category = vpr_get_category(material['categories'])

    cookie_name = 'vnf-view-' + mid

    # update & get view count
    if cookie_name in request.COOKIES:
        view_count = vpr_get_statistic_data(mid, material['version'], 'counter')
    else:
        view_count = voer_add_view_count(mid, material['version'])

    material['view_count'] = view_count

    favorite_count = vpr_get_statistic_data(mid, material['version'], 'favorites')
    material['favorite_count'] = favorite_count

    file_data = []
    file_attachments = vpr_get_statistic_data(mid, material['version'], 'mfiles')
    for file_attachment_id in file_attachments:
        attachment_info = voer_get_attachment_info(file_attachment_id)

        image_mime_type = ['image/gif', 'image/jpeg', 'image/png', 'image/bmp', 'image/tiff', 'image/jp2', 'image/iff']
        if attachment_info['mime_type'] not in image_mime_type:
            file_tmp = {}
            file_tmp['title'] = attachment_info['name']
            file_tmp['attachment_id'] = file_attachment_id
            file_data.append(file_tmp)

    response = render(request, "frontend/module_detail.html",
                      {"material": material, "author": author, "category": category, 'file_data': file_data})

    if cookie_name not in request.COOKIES:
        max_age = settings.VPW_SESSION_MAX_AGE * 24 * 60 * 60
        response.set_cookie(cookie_name, True, max_age)

    return response


def collection_detail(request, title, cid, mid):
    # Get collection
    collection = vpr_get_material(cid)
    outline = json.loads(collection['text'])

    cookie_name = 'vnf-view-' + cid

    # update & get view count
    if cookie_name in request.COOKIES:
        view_count = vpr_get_statistic_data(cid, collection['version'], 'counter')
    else:
        view_count = voer_add_view_count(cid, collection['version'])

    collection['view_count'] = view_count

    favorite_count = vpr_get_statistic_data(cid, collection['version'], 'favorites')
    collection['favorite_count'] = favorite_count

    if not mid:
        # get the first material of collection
        mid = get_first_material_id(outline['content'])
    print mid
    # Get material in collection
    if mid:
        material = vpr_get_material(mid)
        if 'material_id' in material:
            # lay anh trong noi dung
            list_images = vpr_get_material_images(mid)
            # content = re.sub(r'<img[^>]*src="([^"]*)"', _get_image(list_images), material['text'])
            if "text" in material:
                content = re.sub(r'<img[^>]*src="([^"]*)"', _get_image(list_images), material['text'])
                material['text'] = content

            file_data = []
            file_attachments = vpr_get_statistic_data(mid, material['version'], 'mfiles')
            for file_attachment_id in file_attachments:
                attachment_info = voer_get_attachment_info(file_attachment_id)

                image_mime_types = ['image/gif', 'image/jpeg', 'image/png', 'image/bmp', 'image/tiff', 'image/jp2',
                                    'image/iff']
                if attachment_info['mime_type'] not in image_mime_types:
                    file_tmp = {}
                    file_tmp['title'] = attachment_info['name']
                    file_tmp['attachment_id'] = file_attachment_id
                    file_data.append(file_tmp)
        else:
            file_data = []
    else:
        material = {}
        file_data = []

    # Generate outline html
    strOutline = "<ul id='outline-collection' class='list-module-name-content'>%s</ul>" % get_outline(cid, outline[
        'content'])

    # Lay thong tin tac gia bao gom ca thong ke
    author = []
    if 'author' in collection and collection['author']:
        author_id_list = collection['author'].split(',')

        for pid in author_id_list:
            pid = pid.strip()
            person = vpr_get_person(pid, True)
            if person:
                author.append(person)

    category = vpr_get_category(collection['categories'])

    response = render(request, "frontend/collection_detail.html", {"collection": collection, "material": material, "author": author,
                       "category": category, "outline": strOutline, 'file_data': file_data})

    if cookie_name not in request.COOKIES:
        max_age = settings.VPW_SESSION_MAX_AGE * 24 * 60 * 60
        response.set_cookie(cookie_name, True, max_age)

    return response


@login_required
def user_module_detail(request, mid):
    try:
        material = Material.objects.get(id=mid)
        # Chi co tac gia moi vao xem duoc bai
        if material.creator_id != request.user.id:
            raise PermissionDenied
        author_id = request.user.author.author_id
        author = vpr_get_person(author_id, True)
        authors = [author]
        category = vpr_get_category(material.categories)
        if material.type == MODULE_TYPE:
            return render(request, "frontend/module_detail.html", {
                "material": material, "author": authors, "category": category
            })
        else:
            raise PermissionDenied
    except Material.DoesNotExist:
        raise PermissionDenied


@login_required
def user_collection_detail(request, cid, mid):
    try:
        collection = Material.objects.get(id=cid)

        # Chi co tac gia moi vao xem duoc bai
        if collection.creator_id != request.user.id:
            raise PermissionDenied
        author_id = request.user.author.author_id
        author = vpr_get_person(author_id)
        authors = [author]
        category = vpr_get_category(collection.categories)

        outline = json.loads(collection.text)
        if not mid:
            # get the first material of collection
            mid = get_first_material_id(outline['content'])

        # Get material in collection
        if mid:
            material = vpr_get_material(mid)
            # lay anh trong noi dung
            list_images = vpr_get_material_images(mid)
            # content = re.sub(r'<img[^>]*src="([^"]*)"', _get_image(list_images), material['text'])
            if "text" in material:
                content = re.sub(r'<img[^>]*src="([^"]*)"', _get_image(list_images), material['text'])
                material['text'] = content
        else:
            material = {}
            file_data = []

        # Generate outline html
        str_outline = "<ul id='outline-collection' class='list-module-name-content'>%s</ul>" % get_outline(cid, outline['content'], True)

        if collection.type == COLLECTION_TYPE:
            return render(request, "frontend/collection_detail.html", {
                "material": material,
                "collection": collection,
                "author": authors,
                "category": category,
                "outline": str_outline
            })
        else:
            raise PermissionDenied
    except Material.DoesNotExist:
        raise PermissionDenied


@login_required
def create_module(request):
    form = ModuleCreationForm(request.POST or None)
    pid = request.user.author.author_id
    author = vpr_get_person(pid)
    language = get_language()
    params = {}
    current_step = 1

    if request.method == "GET":
        params['license'] = get_setting_value('module_license', language)

    if request.method == "POST":
        try:
            previous_step = int(request.POST.get("step", "0"))
        except ValueError:
            previous_step = 0

        categories_list = vpr_get_categories()
        if previous_step == 1:
            if not request.POST.get("agree"):
                errors = _('You must agree to the terms and conditions!')
                params['errors'] = errors
                params['license'] = get_setting_value('module_license', language)
            else:
                current_step = 2
                params['categories'] = categories_list
                params['author'] = author
        elif previous_step == 2:
            # Save metadata
            if form.is_valid():
                material = _save_material(form, MODULE_TYPE, request.user)
                params['material'] = material
                params['categories'] = categories_list
                params['form'] = form
                if material.id:
                    current_step = 3
                else:
                    # Save khong thanh cong
                    current_step = 2
            else:
                current_step = 2
                params['categories'] = categories_list
                params['author'] = author
                params['form'] = form
        elif previous_step == 3:
            action = request.POST.get("action", "")
            if action == 'import':
                if 'document_file' in request.FILES:
                    upload_file = request.FILES['document_file']
                    upload_filename = normalize_string(upload_file.name)
                    with open(settings.MEDIA_ROOT + '/' + upload_filename, 'wb+') as destination:
                        for chunk in upload_file.chunks():
                            destination.write(chunk)
                    # call import vpt
                    result_import = vpt_import(settings.MEDIA_ROOT + '/' + upload_filename)
                    task_id = result_import['task_id']
                    download_url = vpt_get_url(task_id)
                    response = vpt_download(download_url)
                    # save downloaded file to transforms directory
                    # TODO: transforms dir name should be in settings
                    download_dir = '%s/transforms' % settings.MEDIA_ROOT
                    download_filename = download_url.split('/')[-1]
                    download_filepath = '%s/%s' % (download_dir, download_filename)
                    with open(download_filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk: # filter out keep-alive new chunks
                                f.write(chunk)
                                f.flush()

                    # load downloaded zip file
                    zip_archive = zipfile.ZipFile(download_filepath, 'r')
                    # Unzip into a new directory
                    filename, extension = os.path.splitext(download_filename)
                    extract_path = os.path.join(download_dir, filename)
                    os.mkdir(extract_path)
                    zip_archive.extractall(path=extract_path)

                    # get transformed html content
                    content = open(extract_path + '/index.html', 'r').read()
                    # fix images' urls
                    images = [f.filename for f in zip_archive.filelist if f.filename != 'index.html']
                    for image in images:
                        old_src = 'src="%s"' % image
                        # TODO: transforms dir name should be in settings
                        new_src = 'src="%stransforms/%s/%s"' % (settings.MEDIA_URL, filename, image)
                        content = content.replace(old_src, new_src)

                    form = ModuleCreationForm(request.POST)
                    # set form body
                    form.data['body'] = content

                current_step = 3
                params['categories'] = categories_list
                mid = request.POST.get('mid', '')
                try:
                    material = Material.objects.get(id=mid)
                    params['material'] = material
                except Material.DoesNotExist:
                    pass
                params['form'] = form
                # TODO: nen truyen ca matrial
            elif action == 'save':
                #Save to workspace of current user
                try:
                    mid = int(request.POST.get("mid"))
                except ValueError:
                    mid = 0
                try:
                    if form.is_valid():
                        material = Material.objects.get(id=mid)
                        material.text = form.cleaned_data['body']
                        material.save()
                        return redirect('user_module_detail', mid=mid)
                except Material.DoesNotExist:
                    current_step = 2
                    params['form'] = form
                    params['categories'] = categories_list
            elif action == 'publish':
                try:
                    mid = int(request.POST.get("mid"))
                except ValueError:
                    mid = 0
                try:
                    if form.is_valid():
                        material = Material.objects.get(id=mid)
                        material.text = form.cleaned_data['body']
                        # save_post_to_object(request, material)
                        material.save()
                        # Publish content to VPR
                        result = _publish_material(material)
                        if 'material_id' in result:
                            material.material_id = result['material_id']
                            material.version = result['version']
                            material.save()
                            return redirect('module_detail', title=normalize_string(material.title),
                                            mid=result['material_id'])
                except Material.DoesNotExist:
                    current_step = 2
                    params['form'] = form
                    params['categories'] = categories_list
    return render(request, MODULE_TEMPLATES[current_step], params)


@login_required
def create_collection(request):
    form = CollectionCreationForm(request.POST or None)
    pid = request.user.author.author_id
    author = vpr_get_person(pid)
    language = get_language()
    current_step = 1
    params = {}

    if request.method == "GET":
        params['license'] = get_setting_value('collection_license', language)

    if request.method == "POST":
        action = request.POST.get("action", "")
        try:
            previous_step = int(request.POST.get('step', '0'))
        except ValueError:
            previous_step = 0

        categories_list = vpr_get_categories()
        if previous_step == 1:
            if not request.POST.get("agree"):
                errors = _('You must agree to the terms and conditions!')
                params['errors'] = errors
                params['license'] = get_setting_value('collection_license', language)
            else:
                current_step = 2
                params['categories'] = categories_list
                params['author'] = author
        elif previous_step == 2:
            if action == 'back':
                current_step = 1
            else:
                if form.is_valid():
                    material = _save_material(form, COLLECTION_TYPE, request.user)
                    params['form'] = form
                    params['categories'] = categories_list
                    if material.id:
                        params['material'] = material
                        current_step = 3
                    else:
                        # Save khong thanh cong
                        params['author'] = author
                        current_step = 2
                else:
                    current_step = 2
                    params['form'] = form
                    params['author'] = author
                    params['categories'] = categories_list
        elif previous_step == 3:
            try:
                mid = int(request.POST.get("mid"))
            except ValueError:
                current_step = 1
            if action == "save":
                if form.is_valid():
                    material = Material.objects.get(id=mid)
                    outline = json.loads(form.cleaned_data['body'])
                    tmp = {'content': []}
                    for item in outline[0]['children']:
                        tmp['content'].append(_transform_outline_to_vpr(item))
                    outline_format = json.dumps(tmp)
                    material.text = outline_format
                    material.save()
                    return redirect('user_collection_detail', cid=mid)
                else:
                    current_step = 2
            elif action == "publish":
                if form.is_valid():
                    material = Material.objects.get(id=mid)
                    outline = json.loads(form.cleaned_data['body'])
                    tmp = {'content': []}
                    for item in outline[0]['children']:
                        tmp['content'].append(_transform_outline_to_vpr(item))
                    outline_format = json.dumps(tmp)
                    material.text = outline_format
                    material.save()
                    result = _publish_material(material)
                    if 'material_id' in result:
                        material.material_id = result['material_id']
                        material.version = result['version']
                        material.save()
                        return redirect('collection_detail', title=normalize_string(material.title),
                                        cid=result['material_id'])

            elif action == "back":
                current_step = 2
        else:
            current_step = 1

    return render(request, COLLECTION_TEMPLATES[current_step], params)


def _publish_material(material):
    result = vpr_create_material(
        material_type=material.type,
        text=material.text,
        version=1,
        title=material.title,
        description=material.description,
        categories=material.categories,
        author=material.author,
        editor=material.editor,
        licensor=material.licensor,
        keywords=material.keywords,
        language=material.language,
        license_id=1
    )
    return result


def _save_material(form, material_type, current_user):
    if form.cleaned_data['mid']:
        material = Material.objects.get(id=form.cleaned_data['mid'])
    else:
        material = Material()
    material.title = form.cleaned_data['title']
    material.description = form.cleaned_data['description']
    material.keywords = form.cleaned_data['keywords']
    material.categories = form.cleaned_data['categories']
    material.language = form.cleaned_data['language']
    material.author = form.cleaned_data['authors']
    material.editor = form.cleaned_data['editors']
    material.licensor = form.cleaned_data['licensors']
    material.maintainer = form.cleaned_data['maintainers']
    material.translator = form.cleaned_data['translators']
    material.coeditor = form.cleaned_data['coeditors']
    material.version = form.cleaned_data['version']
    material.material_id = form.cleaned_data['material_id']
    # get current user
    material.creator = current_user
    material.type = material_type
    material.save()
    return material


def view_profile(request, pid):
    page = int(request.GET.get('page', 1))
    current_person = vpr_get_person(pid, True)
    materials = vpr_materials_by_author(pid, page)
    pager = pager_default_initialize(materials['count'], 12, page)
    page_query = get_page_query(request)
    categories = vpr_get_categories()

    person_materials = []
    for material in materials['results']:
        author_id_list = material['author'].split(',')

        p_list = []
        for pid in author_id_list:
            pid = pid.strip()
            person = vpr_get_person(pid)
            if person['fullname']:
                p_list.append({'pid': pid, 'pname': person['fullname']})
            else:
                p_list.append({'pid': pid, 'pname': person['fullname']})
        material['author_list'] = p_list

        view_count = vpr_get_statistic_data(material['material_id'], material['version'], 'counter')
        material['view_count'] = view_count

        favorite_count = vpr_get_statistic_data(material['material_id'], material['version'], 'favorites')
        material['favorite_count'] = favorite_count

        person_materials.append(material)

    return render_to_response("frontend/profile.html",
                              {"person": current_person, "materials": person_materials, 'pager': pager,
                               'page_query': page_query, 'categories': categories},
                              context_instance=RequestContext(request))


def delete_profile(request, pid):
    if not request.user.is_superuser:
        raise PermissionDenied
    result = vpr_delete_person(pid)
    if result == "204":
        print "Xoa thanh cong!"
    return HttpResponseRedirect('/')


'''
Browse page
'''


def browse(request):
    page = int(request.GET.get('page', 1))
    categories = vpr_get_categories()

    cats = request.GET.get("categories", "")
    types = request.GET.get("types", "")
    languages = request.GET.get("languages", "")

    materials = vpr_browse(page=page, categories=cats, types=types, languages=languages)
    material_result = []
    for material in materials['results']:
        view_count = vpr_get_statistic_data(material['material_id'], material['version'], 'counter')
        material['view_count'] = view_count

        favorite_count = vpr_get_statistic_data(material['material_id'], material['version'], 'favorites')
        material['favorite_count'] = favorite_count
        material_result.append(material)

    pager = pager_default_initialize(materials['count'], 12, page)
    page_query = get_page_query(request)

    return render(request, "frontend/browse.html",
                  {"materials": material_result, "categories": categories, 'pager': pager, 'page_query': page_query})


def vpw_authenticate(request):
    username = request.POST['username']
    password = request.POST['password']
    print username + "|" + password
    user = authenticate(username=username, password=password)

    response_data = {}
    response_data['status'] = False
    response_data['message'] = 'The username or password is incorrect.'

    if user is not None:
        if user.is_active:
            login(request, user)
            response_data['status'] = True

    if request.is_ajax():
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


def vpw_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def user_dashboard(request):
    page = int(request.GET.get('page', 1))
    sort_on = request.GET.get('sort', '')
    current_user = request.user
    pid = current_user.author.author_id
    author = vpr_get_person(pid, True)
    materials = vpr_materials_by_author(pid, page, sort_on)

    page_query = get_page_query(request)
    pager = pager_default_initialize(materials['count'], 12, page)

    person_materials = []
    for material in materials['results']:
        view_count = vpr_get_statistic_data(material['material_id'], material['version'], 'counter')
        material['view_count'] = view_count

        favorite_count = vpr_get_statistic_data(material['material_id'], material['version'], 'favorites')
        material['favorite_count'] = favorite_count

        person_materials.append(material)

    return render(request, "frontend/user_profile.html",
                  {"materials": person_materials, "author": author, 'pager': pager, 'page_query': page_query})


@login_required
def mostViewedView(request):
    #page = int(request.GET.get('page', 1))
    current_user = request.user
    pid = current_user.author.author_id
    author = vpr_get_person(pid, True)
    materials = vpr_request('GET', 'stats/materials/counter/')
    template = "frontend/material_stats.html"
    return render(request, template, 
        {"materials": materials, 
         "author": author,
         "title": "Top 12 Most Viewed Documents",
        })


@login_required
def mostFavedView(request):
    #page = int(request.GET.get('page', 1))
    current_user = request.user
    pid = current_user.author.author_id
    author = vpr_get_person(pid, True)
    materials = vpr_request('GET', 'stats/materials/favorites/')
    template = "frontend/material_stats.html"
    return render(request, template, 
        {"materials": materials, 
         "author": author,
         "title": "Top 12 Most Favorited Documents",
        })


@csrf_exempt
def search_result(request):
    keyword = request.REQUEST.get('keyword', '')
    page = int(request.GET.get('page', 1))

    page_query = get_page_query(request)

    search_results = vpr_search(keyword, page)
    pager = pager_default_initialize(search_results['count'], 12, page)
    search_results = search_results['results']

    categories = vpr_get_categories()
    category_dict = {}
    for category in categories:
        category_dict[category['id']] = category['name']

    result_array = []
    for result in search_results:
        if result['user_id']:
            if (result.has_key('fullname') and result['fullname']):
                result['title'] = result['fullname']
            else:
                result['title'] = result['user_id']

            if (result.has_key('affiliation') and result['affiliation']):
                result['description'] = result['affiliation']

        if result.has_key('author'):
            author_array = result['author'].split(',')
            person_list = []
            for pid in author_array:
                pid = pid.strip()
                person = vpr_get_person(pid)
                if person['fullname']:
                    person_list.append({'pid': pid, 'pname': person['fullname']})
                else:
                    person_list.append({'pid': pid, 'pname': person['fullname']})
            result['person_list'] = person_list

        if (result.has_key('categories') and result['categories']):
            category_array = result['categories'].split(',')
            category_list = []
            for cid in category_array:
                cid = cid.strip()
                category_list.append({'cid': cid, 'cname': category_dict.get(int(cid))})

            result['category_list'] = category_list

        if result['material_id']:
            view_count = vpr_get_statistic_data(result['material_id'], result['version'], 'counter')
            result['view_count'] = view_count

            favorite_count = vpr_get_statistic_data(result['material_id'], result['version'], 'favorites')
            result['favorite_count'] = favorite_count

        result_array.append(result)

    return render(request, "frontend/search_result.html",
                  {'keyword': keyword, "search_results": result_array, 'pager': pager, 'page_query': page_query})


def get_pdf(request, mid, version):
    file_name = '%s_%s.pdf' % (mid, version)
    result = vpr_get_pdf(mid, version)
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename=%s' % file_name
    return response


###### UTILITIES FUNCTION #######
def get_first_material_id(outline):
    for item in outline:
        # import pdb;pdb.set_trace()
        if item.has_key('content'):
            return get_first_material_id(item['content'])
        else:
            return item['id']

    return ''


def get_outline(cid, outline, private=False):
    result = ""
    for item in outline:
        print item
        if item['type'] == "module":
            if private:
                result += "<li><a href='/user/c/%s/%s'>%s</a></li>" % (cid, item['id'], item['title'])
            else:
                result += "<li><a href='/c/%s/%s/%s'>%s</a></li>" % (normalize_string(item['title']), cid, item['id'], item['title'])
        else:
            strli = "<li>"
            strli += "<a>%s</a>" % item['title']
            strli += "<ul>"
            strli += get_outline(cid, item['content'], private)
            strli += "</ul>"
            strli += "</li>"
            result += strli

    return result


def pager_default_initialize(count, limit, current_page=1, page_rank=4):
    pager_array = []
    page_total = int(math.ceil((count + limit - 1) / limit))

    if current_page > 1:
        page_temp = {}
        page_temp['text'] = '<<'
        page_temp['value'] = 1
        pager_array.append(page_temp)

        page_temp = {}
        page_temp['text'] = '<'
        page_temp['value'] = current_page - 1
        pager_array.append(page_temp)

    if current_page > page_rank:
        if (current_page - page_rank >= 2):
            page_temp = {}
            page_temp['text'] = '...'
            page_temp['value'] = ''
            pager_array.append(page_temp)

        for i in range(0, page_rank):
            xpage = current_page - page_rank + i

            page_temp = {}
            page_temp['text'] = xpage
            page_temp['value'] = xpage
            pager_array.append(page_temp)
    else:
        for i in range(1, current_page):
            page_temp = {}
            page_temp['text'] = i
            page_temp['value'] = i
            pager_array.append(page_temp)

    page_temp = {}
    page_temp['text'] = current_page
    page_temp['value'] = ''
    pager_array.append(page_temp)

    if (current_page + page_rank < page_total):
        for i in range(1, page_rank + 1):
            xpage = current_page + i
            page_temp = {}
            page_temp['text'] = xpage
            page_temp['value'] = xpage
            pager_array.append(page_temp)

        if (current_page + page_rank + 1 <= page_total):
            page_temp = {}
            page_temp['text'] = '...'
            page_temp['value'] = ''
            pager_array.append(page_temp)
    else:
        for i in range(current_page + 1, page_total + 1):
            page_temp = {}
            page_temp['text'] = i
            page_temp['value'] = i
            pager_array.append(page_temp)

    if current_page < page_total:
        page_temp = {}
        page_temp['text'] = '>'
        page_temp['value'] = current_page + 1
        pager_array.append(page_temp)

        page_temp = {}
        page_temp['text'] = '>>'
        page_temp['value'] = page_total
        pager_array.append(page_temp)

    if len(pager_array) > 1:
        return pager_array

    return []


def get_page_query(request):
    page = request.GET.get('page', 1)
    page_query = request.path.encode("utf8") + "?" + request.META.get('QUERY_STRING').encode("utf8")
    page_query = page_query.replace('&page=' + str(page), '')
    page_query = page_query.replace('?page=' + str(page), '?')

    return page_query

## Browse material
def ajax_browse(request):
    page = int(request.GET.get('page', 1))
    categories = vpr_get_categories()

    cats = request.GET.get("categories", "")
    types = request.GET.get("types", "")
    languages = request.GET.get("languages", "")
    author = request.GET.get("author", "")

    materials = vpr_browse(page=page, categories=cats, types=types, languages=languages, author=author)
    material_result = []
    for material in materials['results']:
        view_count = vpr_get_statistic_data(material['material_id'], material['version'], 'counter')
        material['view_count'] = view_count

        favorite_count = vpr_get_statistic_data(material['material_id'], material['version'], 'favorites')
        material['favorite_count'] = favorite_count
        material_result.append(material)

    if 'count' in materials:
        pager = pager_default_initialize(materials['count'], 12, page)
        page_query = get_page_query(request)

        return render(request, "frontend/ajax/browse.html", {
            "materials": materials, "categories": categories, 'pager': pager, 'page_query': page_query})
    else:
        return HttpResponse("No items found!")


def get_attachment(request, fid):
    attachment_info = voer_get_attachment_info(fid)
    target_url = settings.VPR_URL + '/mfiles/' + fid + '/get/'
    content = urllib.urlopen(target_url).read()
    response = HttpResponse(content, mimetype=attachment_info['mime_type'])
    response['Content-Disposition'] = 'attachment; filename=' + attachment_info['name']

    return response


@login_required
def edit_profile(request):
    current_user = request.user
    pid = current_user.author.author_id
    author = vpr_get_person(pid)
    user = User.objects.get(id=current_user.author.user_id)

    if (request.REQUEST):
        form = EditProfileForm(request.POST)

        author_data = {}
        author_data['id'] = pid
        author_data['user_id'] = author['user_id']
        author_data['email'] = request.POST['email']
        author_data['fullname'] = request.POST['fullname']
        author_data['first_name'] = request.POST['first_name']
        author_data['last_name'] = request.POST['last_name']
        author_data['title'] = request.POST['title']
        author_data['homepage'] = request.POST['homepage']
        author_data['affiliation'] = request.POST['affiliation']
        author_data['affiliation_url'] = request.POST['affiliation_url']
        author_data['biography'] = request.POST['biography']
        author_data['national'] = request.POST['national']

        if form.is_valid():
            if user.check_password(request.POST['current_password']):
                if request.POST['new_password']:
                    user.set_password(request.POST['new_password'])
                    user.save()

                if 'avatar_file' in request.FILES:
                    avatar_file = request.FILES['avatar_file']
                    with open(settings.MEDIA_ROOT + '/' + avatar_file.name, 'wb+') as destination:
                        for chunk in avatar_file.chunks():
                            destination.write(chunk)

                    author_data['avatar'] = settings.MEDIA_ROOT + '/' + avatar_file.name

                result = voer_update_author(author_data)

                if result:
                    author_data = result
                else:
                    author_data['avatar'] = author['avatar']

                # messages.add_message(request, messages.SUCCESS, 'Profile details updated.')
                messages.success(request, 'Profile details updated.')
            else:
                form._errors['current_password'] = form.error_class(['Current password is incorrect'])
        else:
            author_data['avatar'] = author['avatar']

        return render(request, "frontend/user_edit_profile.html", {'author': author_data, 'form': form})

    return render(request, "frontend/user_edit_profile.html", {'author': author})


@login_required
def ajax_add_favorite(request):
    if request.is_ajax():
        current_user = request.user
        pid = current_user.author.author_id

        mid = request.POST['mid']
        version = request.POST['version']

        response_data = {}
        response_data['status'] = False
        response_data['message'] = 'Oops!.'

        result = voer_add_favorite(mid, version, pid)
        if 'favorite' in result:
            response_data['status'] = True
            response_data['message'] = 'Add favorite successful'
            response_data['favorite_count'] = result['favorite']

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        return HttpResponseRedirect('/')


def ajax_search_author(request):
    keyword = request.GET.get('keyword', '')
    result = vpr_search_author(keyword)
    authors = []
    if 'count' in result:
        if result['count'] > 0:
            authors = result['results']
    return HttpResponse(json.dumps(authors), content_type='application/json')


def ajax_search_module(request):
    keyword = request.GET.get('keyword', '')
    result = vpr_search_module(keyword)
    modules = []
    if 'count' in result:
        if result['count'] > 0:
            modules = result['results']
    return HttpResponse(json.dumps(modules), content_type='application/json')


def _transform_outline_to_vpr(outline):
    material_type = outline['attr']['rel']
    result = {}
    if material_type == 'module':
        result['title'] = outline['data']
        tmpid = outline['attr']['id']
        pies = tmpid.split("|")
        result['id'] = pies[0]
        result['version'] = pies[1]
        result['type'] = 'module'
        result['url'] = "http://voer.edu.vn/m/" + result['id'] + "/" + result['version']
        result['license'] = "http://creativecommons.org/licenses/by/3.0/"
    else:
        result['title'] = outline['data']
        result['type'] = 'subcollection'
        result['content'] = []
        if 'children' in outline:
            for item in outline['children']:
                result['content'].append(_transform_outline_to_vpr(item))
    return result


@user_passes_test(lambda u: u.is_superuser)
def admin_import_user(request):
    if (request.REQUEST):
        default_password = request.POST['default_password']

        if not default_password:
            messages.error(request, 'Please enter default password.')
        elif 'user_list' not in request.FILES:
            messages.error(request, 'Please select file')
        else:
            current_user_id_list = []
            current_author_id_list = []

            user_all = User.objects.filter()
            for user in user_all:
                current_user_id_list.append(user.username)
                try:
                    current_author_id_list.append(user.author.author_id)
                except Author.DoesNotExist:
                    print 'no author'

            user_list = request.FILES['user_list']
            file_path = settings.MEDIA_ROOT + '/' + user_list.name
            with open(file_path, 'wb+') as destination:
                for chunk in user_list.chunks():
                    destination.write(chunk)

            file_data = open(file_path, 'rb').read()
            os.remove(file_path)
            user_list = json.loads(file_data)

            user_created_count = 0
            backup_data = []

            for user in user_list:
                csv_data = {}
                insert_into_csv = False
                if user[1]:
                    username = user[1]
                    username = lower(username)
                else:
                    username = 'unknown'

                author_id = user[0]

                if user[0] in current_author_id_list:
                    continue
                else:
                    current_author_id_list.append(user[0])

                if user[1] in current_user_id_list:
                    insert_into_csv = True
                    csv_data['old'] = user

                for i in range(0, 200):
                    if i == 0:
                        tmp_username = username
                    else:
                        tmp_username = username + str(i)

                    if tmp_username not in current_user_id_list:
                        username = tmp_username
                        break

                # Save user
                user = User.objects.create_user(username = username, password = default_password)
                user.save()
                author = Author(user=user)
                author.author_id = author_id
                author.save()

                current_user_id_list.append(username)
                user_created_count = user_created_count + 1

                if insert_into_csv:
                    csv_data['new'] = [author_id, username]

                if csv_data:
                    backup_data.append(csv_data)

            messages.success(request, 'Import user successful.')

            if (user_created_count > 0):
                messages.success(request, '%s user(s) was created.' % user_created_count)

            if backup_data:
                backup_filename = 'backup-'+time.strftime("%Y%m%d%H%M%S")+'.csv'
                csvWriter = csv.writer(open(settings.MEDIA_ROOT + '/' + backup_filename, 'w'))
                csvWriter.writerow(['No.', 'Old data', 'New data'])

                i = 0
                for data in backup_data:
                    i = i + 1
                    csvWriter.writerow([str(i), data['old'], data['new']])

                messages.success(request, '%s user(s) are exist. <a href="/media/%s">(%s)</a>' % (len(backup_data), backup_filename, backup_filename), extra_tags='safe')

    return render(request, "frontend/admin_import_user.html", {})


def admin_featured_materials(request):
    return render(request, "frontend/admin_featured_materials.html", {})


def get_favorite(request):
    current_user = request.user
    pid = current_user.author.author_id
    page = int(request.GET.get('page', 1))

    favorites = vpr_get_favorite(pid, page)

    pager = pager_default_initialize(favorites['count'], 12, page)
    page_query = get_page_query(request)

    favorite_list = []
    for favorite in favorites['results']:
        if favorite['author']:
            author_array = favorite['author'].split(',')
            person_list = []
            for pid in author_array:
                pid = pid.strip()
                person = vpr_get_person(pid)
                if person['fullname']:
                    person_list.append({'pid': pid, 'pname': person['fullname']})
                else:
                    person_list.append({'pid': pid, 'pname': person['user_id']})
            favorite['person_list'] = person_list

        view_count = vpr_get_statistic_data(favorite['material_id'], favorite['version'], 'counter')
        favorite['view_count'] = view_count

        favorite_count = vpr_get_statistic_data(favorite['material_id'], favorite['version'], 'favorites')
        favorite['favorite_count'] = favorite_count

        favorite_list.append(favorite)

    return render(request, "frontend/user_favorite.html", {'materials': favorite_list, 'pager': pager, 'page_query': page_query})


def get_unpublish(request):
    current_user = request.user
    pid = current_user.author.author_id
    author = vpr_get_person(pid)

    sort = request.GET.get('sort', '')
    page = int(request.GET.get('page', 1))

    number_record = 12
    offset = (page - 1) * number_record
    offset_limit = offset + number_record

    try:
        materials = Material.objects.filter(creator_id=current_user.id, material_id='', version=None)
        material_count = len(materials)

        if sort:
            materials = materials.order_by(sort)

        materials = materials[offset: offset_limit]
        pager = pager_default_initialize(material_count, number_record, page)
        page_query = get_page_query(request)

        return render(request, "frontend/user_unpublish.html", {'materials': materials, 'author': author,'pager': pager, 'page_query': page_query})

    except Material.DoesNotExist:
        return HttpResponseRedirect('/')


def ajax_get_similars(request):
    mid = request.GET['mid']
    version = request.GET['version']
    page = int(request.GET.get('page', 1))
    number_record = 4

    prev_page = ''
    next_page = ''
    similar_data = []
    similar_materials = vpr_get_statistic_data(mid, version, 'similar')

    i = 1
    for similar in similar_materials:
        if i < (page - 1) * number_record + 1:
            prev_page = str(page - 1)
            i += 1
            continue

        if i > page * number_record:
            next_page = str(page + 1)
            break

        if similar['material_id']:
            i += 1
            material_tmp = vpr_get_material(similar['material_id'])
            if 'author' in material_tmp:
                author_id_list = material_tmp['author'].split(',')
            else:
                author_id_list = []

            p_list = []
            for pid in author_id_list:
                pid = pid.strip()
                person = vpr_get_person(pid)
                if person['fullname']:
                    p_list.append({'pid': pid, 'pname': person['fullname']})
                else:
                    p_list.append({'pid': pid, 'pname': person['fullname']})
            material_tmp['author_list'] = p_list

            similar_data.append(material_tmp)

    return render(request, "frontend/ajax/similars.html", {'prev_page': prev_page, 'next_page': next_page, 'similar_data': similar_data})


def ajax_get_others(request):
    author_list = request.GET.get('authors', '')
    page = int(request.GET.get('page', 1))
    number_record = 4

    real_page = int(math.ceil((page * number_record + 11) / 12))

    prev_page = ''
    next_page = ''
    other_data = []
    other_materials = vpr_materials_by_author(author_list, real_page)

    if other_materials['next']:
        next_page = str(page + 1)

    if other_materials['previous']:
        prev_page = str(page - 1)

    actual_page = page % 3

    if actual_page == 0:
        actual_page = 3

    i = 1
    for other_material in other_materials['results']:
        if i < (actual_page - 1) * number_record + 1:
            prev_page = str(page - 1)
            i += 1
            continue

        if i > actual_page * number_record:
            next_page = str(page + 1)
            break

        i += 1
        other_data.append(other_material)

    return render(request, "frontend/ajax/others.html", {'prev_page': prev_page, 'next_page': next_page, 'other_data': other_data})

@login_required
def user_module_reuse(request, mid, version=1):
    if version is None:
        version = 1
    material = vpr_get_material(mid, version)
    categories = vpr_get_categories()
    author = vpr_get_person(request.user.author.author_id)
    if request.method == "POST":
        form = ModuleCreationForm(request.POST)
        action = request.POST.get("action", "")
        if action == 'save':
            if form.is_valid():
                material = _save_material(form, MODULE_TYPE, request.user)
                material.text = form.cleaned_data['body']
                material.save()
                return redirect('user_module_detail', mid=material.id)
        elif action == 'publish':
            if form.is_valid():
                material = _save_material(form, MODULE_TYPE, request.user)
                material.text = form.cleaned_data['body']
                material.save()
                # Publish content to VPR
                result = _publish_material(material)
                if 'material_id' in result:
                    material.material_id = result['material_id']
                    material.version = result['version']
                    material.save()
                    return redirect('module_detail', mid=result['material_id'])
    else:
        form = ModuleCreationForm(dict(body=material['text']))
    params = {'material': material, 'categories': categories,
              'form': form, 'author': author}
    return render(request, MODULE_TEMPLATES[3], params)


@user_passes_test(lambda u: u.is_superuser)
def admin_settings(request):
    """
    Settings page for admin
    """
    language = get_language() # current language
    module_license, created = Settings.objects.get_or_create(name='module_license', language=language)
    collection_license, created = Settings.objects.get_or_create(name='collection_license', language=language)

    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            # save module_license's change
            module_license.value = form.cleaned_data['module_license']
            module_license.save()
            # save collection_license's change
            collection_license.value = form.cleaned_data['collection_license']
            collection_license.save()
            messages.success(request, 'Settings updated successfully.')
        else:
            messages.error(request, 'Error while updating settings.')
    else:
        form = SettingsForm(dict(module_license=module_license.value,
                                 collection_license=collection_license.value))

    return render(request, "frontend/admin_settings.html", {'form': form})


def get_content_file(request, fid):
    r = vpr_get_content_file(fid)
    response = HttpResponse(r.content, content_type=r.headers['content-type'])
    return response


def get_setting_value(license_type, language='vi'):
    """
    Get value of a setting by language
    """
    try:
        setting = Settings.objects.get(name=license_type, language=language)
        return setting.value
    except ObjectDoesNotExist:
        return str()


def get_avatar(request, pid):
    r = vpr_get_user_avatar(pid)
    response = HttpResponse(r.content, content_type=r.headers['content-type'])
    return response


def server_error(request):
    # one of the things 'render' does is add 'STATIC_URL' to
    # the context, making it available from within the template.
    response = render(request, "500.html")
    response.status_code = 500
    return response
