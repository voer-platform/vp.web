from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from vpw.vpr_api import vpr_get_material, vpr_get_category, vpr_get_person,\
    vpr_get_categories, vpr_browse, vpr_materials_by_author, vpr_get_pdf
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
import json

# Create your views here.

def home(request):
    material_features = ['64b4a7a7','fd2f579c','f2feed3c','4dbdd6c5','c3ad3533','0e60bfc6']
    materials_list = []
    for mid in material_features:
        material = vpr_get_material(mid)
        materials_list.append(material)

    # Get featured authors
    person_features = [50,76,34,54,23]
    person_list = []
    for pid in person_features:
        person = vpr_get_person(pid)
        person_list.append(person)

    return render(request, "frontend/index.html", {"materials_list": materials_list, "person_list": person_list})

def signup(request):
    return render(request, "frontend/signup.html")

def aboutus(request):
    return render(request, "frontend/aboutus.html")

def module_detail(request, mid, version):
    material = vpr_get_material(mid)
    author = vpr_get_person(material['author'])
    category = vpr_get_category(material['categories'])
    return render(request, "frontend/module_detail.html", {"material": material, "author": author, "category": category})

def collection_detail(request, cid, mid):
    # Get collection
    collection = vpr_get_material(cid)

    if not mid:
        outline = json.loads(collection['text'])
        mid = get_first_material_id(outline['content'])
        # print first_material_id

    # Get material in collection
    material = vpr_get_material(mid)

    author = vpr_get_person(collection['author'])
    category = vpr_get_category(collection['categories'])

    return render(request, "frontend/collection_detail.html", {"material": material, "author": author, "category": category})


def create_module(request):
    step = request.GET.get('step', '')
    print "Step: " + step
    if step == 1:
        return render(request, "frontend/module/create_step1.html")
    elif step == 2:
        return render(request, "frontend/module/create_step2.html")
    elif step == 3:
        return render(request, "frontend/module/create_step3.html")
    else:
        return render(request, "frontend/module/create_step1.html")


def crete_collection(request):
    step = request.GET.get('step', '')
    print "Step: " + step
    if step == 1:
        return render(request, "frontend/collection/create_step1.html")
    elif step == 2:
        return render(request, "frontend/collection/create_step2.html")
    elif step == 3:
        return render(request, "frontend/collection/create_step3.html")
    else:
        return render(request, "frontend/collection/create_step1.html")
    return render(request, "frontend/collection/create_step1.html")

def view_profile(request, pid):
    person = vpr_get_person(pid)
    materials = vpr_materials_by_author(pid)
    return render_to_response("frontend/profile.html", {"person": person, "materials": materials}, context_instance=RequestContext(request))

'''
Browse page
'''
def browse(request):
    categories = vpr_get_categories()

    cats = request.GET.get("categories", "")
    types = request.GET.get("types", "")
    languages = request.GET.get("languages", "")

    materials = vpr_browse(categories=cats, types=types, languages=languages)

    return render(request, "frontend/browse.html", {"materials": materials, "categories": categories})

def vpw_authenticate(request):
    username = request.POST['username']
    password = request.POST['password']
    print username + "|" + password
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            # Return a 'disabled account' error message
            return HttpResponseRedirect('/')
    else:
        # Return an 'invalid login' error message.
        return HttpResponseRedirect('/')

def vpw_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_profile(request):
    return render(request, "frontend/user_profile.html")

def search_result(request):
    return render(request, "frontend/search_result.html")

def get_pdf(request, mid, version):
    # mid = request.GET.get("mid", "")
    # version = request.GET.get("version", "")

    pdf_content = vpr_get_pdf(mid, version)

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


## Browse material
def ajax_browse(request):
    categories = vpr_get_categories()

    cats = request.GET.get("categories", "")
    types = request.GET.get("types", "")
    languages = request.GET.get("languages", "")

    materials = vpr_browse(categories=cats, types=types, languages=languages)

    return render(request, "frontend/ajax/browse.html", {"materials": materials, "categories": categories})
