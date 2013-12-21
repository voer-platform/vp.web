from django.shortcuts import render, redirect
from django.http import HttpResponse
from vpw.vpr_api import vpr_get_material, vpr_get_category, vpr_get_person,\
    vpr_get_categories
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect

# Create your views here.

def home(request):
    material_features = ['64b4a7a7','fd2f579c','f2feed3c','4dbdd6c5','c3ad3533','0e60bfc6']
    materials_list = []
    for mid in material_features:
        material = vpr_get_material(mid)
        materials_list.append(material)

    # Get featured authors
    person_features = []
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

def collection_detail(request, cid, version):
    material = vpr_get_material(cid)
    author = vpr_get_person(material['author'])
    category = vpr_get_category(material['categories'])
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
    return render(request, "frontend/profile.html", {"person": person})

'''
Browse page
'''
def browse(request):
    categories = vpr_get_categories()
    return render(request, "frontend/browse.html", {"categories": categories})

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
