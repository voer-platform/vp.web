'''
Created on 17 Dec 2013

@author: huyvq
'''
from django.conf import settings
import json,httplib

def vpr_request(method, path, body=None):
    connection = httplib.HTTPConnection(settings.VPR_URL, settings.VPR_PORT)
    connection.connect()
    headers = {}
    connection.request(method, "/%s/%s" % (settings.VPR_VERSION, path), body, headers)
    result = json.loads(connection.getresponse().read())
    return result

def vpr_get_categories():
    result = vpr_request("GET", "categories")
    return result;

def vpr_create_category(name, parent, description):
    result = vpr_request("POST", "categories/", json.dumps({
       "name": name,
       "parent": parent,
       "description": description
     }))
    return result

def vpr_get_category(cat_id):
    result = vpr_request("GET", "categories/%s" % cat_id)
    return result;

def vpr_update_category(cat_id, name, parent, description):
    result = vpr_request("PUT", "categories/%s" % cat_id, json.dumps({
        "name": name,
        "parent": parent,
        "description": description
    }))
    return result

def vpr_delete_category(cat_id):
    result = vpr_request("DELETE", "categories/%s" % cat_id)
    return result

def vpr_get_persons():
    result = vpr_request("GET", "persons")
    return result

def vpr_get_person(pid):
    result = vpr_request("GET", "persons/%s" % pid)
    return result

def vpr_get_materials():
    result = vpr_request("GET", "materials")
    return result

def vpr_get_material(mid):
    result = vpr_request("GET", "materials/%s" % mid)
    return result

def vpr_create_material(**kwargs):
    result = vpr_request("POST", "materials", json.dumps({
        "material_type": kwargs.get("material_type", 1),
        "text": kwargs.get("text"),
        "version": kwargs.get("version"),
        "title": kwargs.get("title"),
        "description": kwargs.get("description"),
        "categories": kwargs.get("categories"),
        "author": kwargs.get("author"),
        "editor": kwargs.get("editor"),
        "licensor": kwargs.get("licensor"),
        "keywords": kwargs.get("keywords"),
        "image": kwargs.get("image"),
        "attach01": kwargs.get("attach01"),
        "attach01_name": kwargs.get("attach01_name"),
        "attach01_description": kwargs.get("attach01_description"),
        "attach02": kwargs.get("attach02"),
        "attach02_name": kwargs.get("attach02_name"),
        "attach02_description": kwargs.get("attach02_description"),
        "language": kwargs.get("language"),
        "license_id": kwargs.get("license_id", 1)
    }))

    return result

def vpr_search(keyword):
    result = vpr_request("GET", "search", json.dumps({
            "kw":keyword
        }))
    return result

# Browse materials
def vpr_browse(**kwargs):
    categories = kwargs.get("categories", "")
    types = kwargs.get("types", "")
    languages = kwargs.get("languages", "")
    result = vpr_request("GET", "materials", json.dumps({
            "categories": categories,
            "material_type": types,
            "language": languages
        }))
    return result

def vpr_materials_by_author(aid):
    result = vpr_request("GET", "materials", json.dumps({
            "author": aid
        }))
    return result
