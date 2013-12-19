from django.shortcuts import render
from django.http import HttpResponse
from vpw.vpr_api import vpr_get_material, vpr_get_category, vpr_get_person,\
    vpr_get_categories

# Create your views here.

def home(request):
    features = ['64b4a7a7','fd2f579c','f2feed3c','4dbdd6c5','c3ad3533','0e60bfc6']
    materials_list = []
    for mid in features:
        material = vpr_get_material(mid)
        materials_list.append(material)
        
    return render(request, "frontend/index.html", {"materials_list": materials_list})

def signup(request):
    return render(request, "frontend/signup.html")

def aboutus(request):
    return render(request, "frontend/aboutus.html")

def module_detail(request, mid, version):
    material = vpr_get_material(mid)
    author = vpr_get_person(material['author'])
    category = vpr_get_category(material['categories'])
    return render(request, "frontend/module_detail.html", {"material": material, "author": author, "category": category})

def create_module(request):
    return render(request, "frontend/module/create_step1.html")

def crete_collection(request):
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