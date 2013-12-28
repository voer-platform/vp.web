'''
Created on 17 Dec 2013

@author: huyvq
'''
import os
from django.conf import settings
import json, httplib, urllib
import requests


def vpt_request(method, path, body=None):
    connection = httplib.HTTPConnection(settings.VPT_URL, settings.VPT_PORT)
    connection.connect()
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
    connection.request(method, "/%s" % path, body, headers)
    respond = connection.getresponse().read()

    if method == "DELETE":
        result = connection.getresponse().status
    else:
        try:
            result = json.loads(respond)
        except:
            result = respond
    return result


def vpr_request(method, path, body=None):
    url = settings.VPR_URL + path
    r = requests.request(method, url, data=body)

    if method == "DELETE":
        result = r.status_code
    else:
        try:
            result = json.loads(r.text)
        except:
            result = r
    return result


def vpt_import(file_path):
    import_url = settings.VPT_URL + 'import'
    token = 'a9af1d6ca60243a38eb7d52dd344f7cb'
    cid = 'vietdt'
    payload = {'token': token, 'cid': cid}

    file_name = os.path.basename(file_path)
    file_data = open(file_path, 'rb').read()
    files = {'file': (file_name, file_data)}
    r = requests.post(import_url, files=files, data=payload)
    return r.text


def vpr_get_categories():
    result = vpr_request("GET", "categories")
    return result


def vpr_create_category(name, parent, description):
    result = vpr_request("POST", "categories/", {
        "name": name,
        "parent": parent,
        "description": description
    })
    return result


def vpr_get_category(cat_id):
    result = vpr_request("GET", "categories/%s" % cat_id)
    return result


def vpr_update_category(cat_id, name, parent, description):
    result = vpr_request("PUT", "categories/%s" % cat_id, {
        "name": name,
        "parent": parent,
        "description": description
    })
    return result


def vpr_delete_category(cat_id):
    result = vpr_request("DELETE", "categories/%s" % cat_id)
    return result


def vpr_get_persons():
    result = vpr_request("GET", "persons")
    return result


def vpr_delete_person(pid):
    result = vpr_request("DELETE", "persons/%s" % pid)
    return result


def vpr_get_person(pid, is_count=False):
    if is_count:
        result = vpr_request("GET", "persons/%s?count=1" % pid)
    else:
        result = vpr_request("GET", "persons/%s" % pid)
    return result


def vpr_get_materials():
    result = vpr_request("GET", "materials")
    return result


def vpr_get_material(mid):
    result = vpr_request("GET", "materials/%s" % mid)
    return result


def vpr_create_material(**kwargs):
    result = vpr_request("POST", "materials", {
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
    })

    return result


def vpr_get_pdf(mid, version):
    result = vpr_request('GET', "materials/%s/%s/pdf/" % (mid, version))
    return result


def vpr_search(keyword, page):
    result = vpr_request("GET", "search?kw=%s&page=%s" % (urllib.quote(keyword.encode("utf8")), page))
    return result


# Browse materials
def vpr_browse(**kwargs):
    page = kwargs.get("page", 1)
    categories = kwargs.get("categories", "")
    types = kwargs.get("types", "")
    languages = kwargs.get("languages", "")
    author = kwargs.get("author", "")
    params = ["page=%s" % page]
    # print "Type : " + types
    if categories and categories != "0":
        params.append("categories=%s&or=categories" % categories)

    if types and types != "0" and types != '1,2':
        params.append("material_type=%s" % types)

    if languages and languages != "0" and languages != 'vi,en':
        params.append("language=%s" % languages)

    if author:
        params.append("author=%s" % author)

    params = "&".join(params)

    # print "params: " + params
    result = vpr_request("GET", "materials?names=1&%s" % params)

    #Get information facet
    facet = vpr_request("GET", "facet?%s" % params)
    result['facet'] = facet
    return result


def vpr_materials_by_author(aid, page=1):
    result = vpr_request("GET", "materials?author=%s&page=%s" % (aid, str(page)))
    return result


def vpr_create_person(**kwargs):
    result = vpr_request("POST", "persons/", {
        "fullname": kwargs.get("fullname"),
        "user_id": kwargs.get("user_id"),
        "first_name": kwargs.get("first_name"),
        "last_name": kwargs.get("last_name"),
        "email": kwargs.get("email"),
        # "title": kwargs.get("title"),
        # "homepage": kwargs.get("homepage"),
        # "affiliation": kwargs.get("affiliation"),
        # "affiliation_url": kwargs.get("affiliation_url"),
        # "national": kwargs.get("national"),
        # "biography": kwargs.get("biography"),
        # "client_id": kwargs.get("client_id"),
    })

    return result


def vpr_get_statistic_data(mid, version, field_name):
    if not version:
        result = vpr_request('GET', "materials/%s/%s/" % (mid, field_name))
    else:
        result = vpr_request('GET', "materials/%s/%s/%s/" % (mid, version, field_name))

    return result


def voer_get_attachment_info(attach_id):
    result = vpr_request('GET', "mfiles/%s/" % attach_id)

    return result


def vpr_get_material_images(mid):
    list_ids = vpr_request('GET', 'materials/%s/mfiles/' % mid)
    list_images = {}
    for image_id in list_ids:
        image = vpr_request('GET', 'mfiles/%s' % image_id)
        if 'name' in image:
            list_images[image['name']] = '%smfiles/%s/get' % (settings.VPR_URL, image_id)
    return list_images


def voer_update_author(author):
    result = vpr_request('PUT', "persons/%s/" % author['id'], author)

    return result
