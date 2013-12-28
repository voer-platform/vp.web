import json
import math
import re
import urllib

from django.core.exceptions import PermissionDenied

from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from vpw.models import Material
from vpw.vpr_api import vpr_get_material, vpr_get_category, vpr_get_person, \
    vpr_get_categories, vpr_browse, vpr_materials_by_author, vpr_get_pdf, vpr_search, vpr_delete_person, vpr_get_statistic_data, \
    voer_get_attachment_info,vpt_import, vpr_create_material, vpr_get_material_images, voer_update_author

from vpw.forms import ModuleCreationForm, EditProfileForm

# Create your views here.

def home(request):
    material_features = ['64b4a7a7', 'fd2f579c', 'f2feed3c', '4dbdd6c5', 'c3ad3533', '0e60bfc6']
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
    person_features = [50, 76, 90, 54, 23]
    person_list = []
    for pid in person_features:
        person = vpr_get_person(pid)
        if 'id' in person:
            person_list.append(person)

    return render(request, "frontend/index.html", {"materials_list": materials_list, "person_list": person_list})


def signup(request):
    return render(request, "frontend/signup.html")


def aboutus(request):
    return render(request, "frontend/aboutus.html")


def _get_image(list_images):
    def replace_image(match_object):
        return "<img src='" + list_images[match_object.group(1)] + "'"
    return replace_image


def module_detail(request, mid, version):
    material = vpr_get_material(mid)
    # lay anh trong noi dung
    list_images = vpr_get_material_images(mid)
    # content = re.sub(r'<img[^>]*src="([^"]*)"', _get_image(list_images), material['text'])
    content = re.sub(r'<img[^>]*src="([^"]*)"', _get_image(list_images), material['text'])
    material['text'] = content

    other_data = []
    if (material.has_key('author') and material['author']):
        author = vpr_get_person(material['author'])
        other_materials = vpr_materials_by_author(material['author'])
        i = 1
        for other_material in other_materials['results']:
            if i > 4:
                break

            i = i + 1
            other_data.append(other_material)
    else:
        author = {}

    category = vpr_get_category(material['categories'])

    view_count = vpr_get_statistic_data(mid, material['version'], 'counter')
    material['view_count'] = view_count

    favorite_count = vpr_get_statistic_data(mid, material['version'], 'favorites')
    material['favorite_count'] = favorite_count

    similar_data = []
    similar_materials = vpr_get_statistic_data(mid, material['version'], 'similar')
    i = 1
    for similar in similar_materials:
        if i > 4:
            break

        i = i + 1
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

    file_data = []
    file_attachments = vpr_get_statistic_data(mid, material['version'], 'mfiles')
    for file_attachment_id in file_attachments:
        attachment_info = voer_get_attachment_info(file_attachment_id)

        if attachment_info['mime_type'] != 'image/jpeg':
            file_tmp = {}
            file_tmp['title'] = attachment_info['name']
            file_tmp['attachment_id'] = file_attachment_id
            file_data.append(file_tmp)

    return render(request, "frontend/module_detail.html",
                  {"material": material, "author": author, "category": category, 'other_data': other_data, 'similar_data': similar_data, 'file_data': file_data})


def collection_detail(request, cid, mid):
    # Get collection
    collection = vpr_get_material(cid)
    outline = json.loads(collection['text'])

    view_count = vpr_get_statistic_data(cid, collection['version'], 'counter')
    collection['view_count'] = view_count

    favorite_count = vpr_get_statistic_data(cid, collection['version'], 'favorites')
    collection['favorite_count'] = favorite_count

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

        file_data = []
        file_attachments = vpr_get_statistic_data(mid, material['version'], 'mfiles')
        for file_attachment_id in file_attachments:
            attachment_info = voer_get_attachment_info(file_attachment_id)

            if attachment_info['mime_type'] != 'image/jpeg':
                file_tmp = {}
                file_tmp['title'] = attachment_info['name']
                file_tmp['attachment_id'] = file_attachment_id
                file_data.append(file_tmp)
    else:
        material = {}
        file_data = []

    # Generate outline html
    strOutline = "<ul class='list-module-name-content'>%s</ul>" % get_outline(cid, outline['content'])

    author = vpr_get_person(collection['author'])
    category = vpr_get_category(collection['categories'])

    other_data = []
    other_materials = vpr_materials_by_author(collection['author'])
    i = 1
    for other_material in other_materials['results']:
        if i > 4:
            break

        i = i + 1
        other_data.append(other_material)

    similar_data = []
    similar_materials = vpr_get_statistic_data(cid, collection['version'], 'similar')
    i = 1
    for similar in similar_materials:
        if i > 4:
            break

        i = i + 1
        material_tmp = vpr_get_material(similar['material_id'])

        if (material_tmp.has_key('author') and material_tmp['author']):
            author_id_list = material_tmp['author'].split(',')

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

    return render(request, "frontend/collection_detail.html",
                  {"collection": collection, "material": material, "author": author, "category": category,
                   "outline": strOutline, 'other_data': other_data, 'similar_data': similar_data, 'file_data': file_data})


@login_required
def document_detail(request, did):
    try:
        material = Material.objects.get(id=did)
        # Chi co tac gia moi vao xem duoc bai
        if material.creator_id != request.user.id:
            raise PermissionDenied
        author_id = request.user.author.author_id
        author = vpr_get_person(author_id)
        category = vpr_get_category(material.categories)
        if material.type == 1:
            return render(request, "frontend/module_detail.html", {
                "material": material, "author": author, "category": category
            })
        elif material.type == 2:
            render(request, "frontend/collection_detail.html", {
                "material": material, "author": author, "category": category
            })
        else:
            raise PermissionDenied
    except Material.DoesNotExist:
        raise PermissionDenied


@login_required
def create_module(request):
    if request.method == "POST":
        try:
            current_step = int(request.POST.get("step", "0"))
        except ValueError:
            current_step = 0

        categories_list = vpr_get_categories()
        if current_step == 1:
            return render(request, "frontend/module/create_step2.html", {"categories": categories_list})

        form = ModuleCreationForm(request.POST)
        if current_step == 2:
            # Save metadata
            if form.is_valid():
                material = Material()
                material.title = form.cleaned_data['title']
                material.description = form.cleaned_data['description']
                material.keywords = form.cleaned_data['keywords']
                material.categories = form.cleaned_data['categories']
                material.language = form.cleaned_data['language']
                #get current user
                material.creator = request.user
                material.type = 1
                material.save()
                # material = Material.objects.get(id=1)
                if material.id:
                    return render(request, "frontend/module/create_step3.html",
                                  {"material": material, "categories": categories_list, 'form': form})
            else:
                return render(request, "frontend/module/create_step2.html",
                              {"categories": categories_list, 'form': form})

        if current_step == 3:
            action = request.POST.get("action", "")
            if action == 'import':
                upload_file = request.FILES['document_file']
                with open(settings.MEDIA_ROOT + '/' + upload_file.name, 'wb+') as destination:
                    # for chunk in upload_file.chunks():
                    #     destination.write(chunk)
                    # call import vpt
                    result_import = vpt_import(settings.MEDIA_ROOT + '/' + upload_file.name)
                    status = result_import['status']
                    task_id = result_import['task_id']

                form = ModuleCreationForm(request.POST)
                return render(request, "frontend/module/create_step3.html",
                              {"material": material, "categories": categories_list, 'form': form})
            if action == 'save':
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
                        return redirect('document_detail', did=mid)
                except Material.DoesNotExist:
                    pass
            if action == 'publish':
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
                        result = vpr_create_material(
                            material_type=material.type,
                            text=material.text,
                            version=1,
                            title=material.title,
                            description=material.description,
                            categories=material.categories,
                            author="50",
                            editor="",
                            licensor="",
                            keywords=material.keywords,
                            language=material.language,
                            license_id=1
                        )
                        if 'material_id' in result:
                            return redirect('module_detail', mid=result['material_id'])
                except Material.DoesNotExist:
                    pass
            #Save content & metadata, or publish to VPR
            pass
    return render(request, "frontend/module/create_step1.html")


@login_required
def create_collection(request):
    form = CollectionCreationForm(request.POST or None)
    if request.method == "POST":
        try:
            previous_step = int(request.POST.get('step', '0'))
        except ValueError:
            previous_step = 0

        if previous_step == 1:
            return render(request, "frontend/collection/create_step2.html")
        elif previous_step == 2:
            return render(request, "frontend/collection/create_step3.html", {
                'form': form
            })
        else:
            return render(request, "frontend/collection/create_step1.html")
    else:
        return render(request, "frontend/collection/create_step1.html")


def view_profile(request, pid):
    page = int(request.GET.get('page', 1))
    current_person = vpr_get_person(pid, True)
    materials = vpr_materials_by_author(pid, page)
    pager = pager_default_initialize(materials['count'], 12, page)
    page_query = get_page_query(request)

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

    return render_to_response("frontend/profile.html", {"person": current_person, "materials": person_materials, 'pager': pager, 'page_query': page_query},
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

    return render(request, "frontend/browse.html", {"materials": material_result, "categories": categories, 'pager': pager, 'page_query': page_query})


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
    current_user = request.user
    pid = current_user.author.author_id
    author = vpr_get_person(pid, True)
    materials = vpr_materials_by_author(pid, page)

    page_query = get_page_query(request)
    pager = pager_default_initialize(materials['count'], 12, page)

    person_materials = []
    for material in materials['results']:
        view_count = vpr_get_statistic_data(material['material_id'], material['version'], 'counter')
        material['view_count'] = view_count

        favorite_count = vpr_get_statistic_data(material['material_id'], material['version'], 'favorites')
        material['favorite_count'] = favorite_count

        person_materials.append(material)

    return render(request, "frontend/user_profile.html", {"materials": person_materials, "author": author, 'pager': pager, 'page_query': page_query})


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

    return render(request, "frontend/search_result.html", {'keyword': keyword, "search_results": result_array, 'pager': pager, 'page_query': page_query})


def get_pdf(request, mid, version):
    # mid = request.GET.get("mid", "")
    # version = request.GET.get("version", "")

    pdf_content = vpr_get_pdf(mid, version)
    print pdf_content
    return HttpResponse(pdf_content, mimetype='application/pdf')


###### UTILITIES FUNCTION #######
def get_first_material_id(outline):
    for item in outline:
        # import pdb;pdb.set_trace()
        if item.has_key('content'):
            return get_first_material_id(item['content'])
        else:
            return item['id']

    return ''


def get_outline(cid, outline):
    result = ""
    for item in outline:
        print item
        if item['type'] == "module":
            result += "<li><a href='/c/%s/%s'>%s</a></li>" % (cid, item['id'], item['title'])
        else:
            strli = "<li>"
            strli += "<a>%s</a>" % item['title']
            strli += "<ul>"
            strli += get_outline(cid, item['content'])
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
    else :
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

        if (current_page + page_rank + 2 <= page_total):
            page_temp = {}
            page_temp['text'] = '...'
            page_temp['value'] = ''
            pager_array.append(page_temp)
    else :
        for i in range(current_page+1, page_total+1):
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

    if len(pager_array) > 1 :
        return pager_array

    return []

def get_page_query(request):
    page = request.GET.get('page', 1)
    page_query = request.path.encode("utf8") + "?" + request.META.get('QUERY_STRING').encode("utf8")
    page_query = page_query.replace('&page=' + str(page), '')

    return page_query

## Browse material
def ajax_browse(request):
    page = int(request.GET.get('page', 1))
    categories = vpr_get_categories()

    cats = request.GET.get("categories", "")
    types = request.GET.get("types", "")
    languages = request.GET.get("languages", "")

    materials = vpr_browse(page=page, categories=cats, types=types, languages=languages)
    if 'count' in materials:
        pager = pager_default_initialize(materials['count'], 12, page)
        page_query = get_page_query(request)

        return render(request, "frontend/ajax/browse.html", {
            "materials": materials, "categories": categories, 'pager': pager, 'page_query': page_query})
    else:
        return HttpResponse("No items found!")


def get_attachment(request, fid):
    attachment_info = voer_get_attachment_info(fid)
    target_url = 'http://' + settings.VPR_URL + ':' + settings.VPR_PORT + '/' + settings.VPR_VERSION + '/mfiles/' + fid + '/get/'
    content = urllib.urlopen(target_url).read()
    response = HttpResponse(content, mimetype=attachment_info['mime_type'])
    response['Content-Disposition'] = 'attachment; filename='+attachment_info['name']

    return response


@login_required
def edit_profile(request):
    current_user = request.user
    pid = current_user.author.author_id
    author = vpr_get_person(pid)

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
            avatar_file = request.FILES['avatar_file']
            voer_update_author(author_data)

        return render(request, "frontend/user_edit_profile.html", {'author': author_data, 'form': form})

    return render(request, "frontend/user_edit_profile.html", {'author': author})

