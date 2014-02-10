'''
Created on 17 Dec 2013

@author: huyvq
'''
import time
import os
from django.conf import settings
import json, httplib, urllib
import requests
from django.core.urlresolvers import reverse


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
    return json.loads(r.text)


def vpt_check_status(task_id):
    """
    request import status by task id
    """
    import_url = '%simport' % settings.VPT_URL
    r = requests.get(import_url, params={'task_id': task_id})
    # TODO: check status_code for errors
    return json.loads(r.text)


def vpt_get_url(task_id):
    """
    ping status continuosly to get download url
    """
    # TODO: should perform at client side
    # TODO: should put these defaults in settings
    retry = 20
    interval = 5

    n = 0
    while n < retry:
        result = vpt_check_status(task_id)
        if result.has_key('url'):
            return result['url']
        # pause a few second before continue
        time.sleep(interval)
        n += 1


def vpt_download(url):
    """
    download transformed file
    """
    r = requests.get(url, stream=True)
    return r


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


def vpr_get_material(mid, version=1):
    result = vpr_request("GET", "materials/%s/%s" % (mid, version))
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
    url = settings.VPR_URL + "materials/%s/%s/pdf/" % (mid, version)
    r = requests.request("GET", url)

    retry = 20
    interval = 5

    n = 0
    while n < retry:
        r = requests.request("GET", url)
        if r.status_code == 200:
            return r.content
        # pause a few second before continue
        time.sleep(interval)
        n += 1
    return


def vpr_search(**kwargs):
    keyword = kwargs.get('keyword', '')
    page = kwargs.get("page", 1)
    search_type = kwargs.get('search_type', '')
    material_type = kwargs.get('material_type', '')

    search_string = "search?kw=%s&page=%s"
    if search_type == "m":
        search_string += "&on=m"
    elif search_type == "p":
        print "fajsfjagf"
        search_string += "&on=p"

    if material_type != "":
        search_string += "&type=" + material_type

    result = vpr_request("GET", search_string % (urllib.quote(keyword.encode("utf8")), page))
    return result


# Browse materials
def vpr_browse(**kwargs):
    page = kwargs.get("page", 1)
    categories = kwargs.get("categories", "")
    types = kwargs.get("types", "")
    languages = kwargs.get("languages", "")
    author = kwargs.get("author", "")
    sort = kwargs.get("sort", "title")
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

    params.append("sort_on=%s" % sort)
    params = "&".join(params)

    # print "params: " + params
    result = vpr_request("GET", "materials?names=1&%s" % params)

    #Get information facet
    facet = vpr_request("GET", "facet?%s" % params)
    result['facet'] = facet
    return result


def vpr_materials_by_author(aid, page=1, sort_on=''):
    result = vpr_request("GET", "materials?author=%s&page=%s&sort_on=%s" % (aid, str(page), sort_on))
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
            list_images[image['name']] = '/file/%s' % image_id
    return list_images


def voer_update_author(author):
    url = settings.VPR_URL
    files = {}
    if 'avatar' in author:
        file_path = author['avatar']
        del author['avatar']

        file_name = os.path.basename(file_path)
        file_data = open(file_path, 'rb').read()
        files = {'avatar': (file_name, file_data)}

        os.remove(file_path)

    r = requests.put(url + 'persons/%s/' % author['id'], files=files, data=author)

    if r.status_code == 200:
        result = json.loads(r.text)
    else:
        result = {}

    return result


def voer_add_favorite(mid, version, pid):
    if not version:
        result = vpr_request('POST', "materials/%s/favorites" % mid, {'person': pid})
    else:
        result = vpr_request('POST', "materials/%s/%s/favorites" % (mid, version), {'person': pid})

    return result


def vpr_get_favorite(pid, page=1):
    result = vpr_request("GET", "persons/%s/favorites/?page=%s" % (pid, str(page)))
    return result


def vpr_search_author(author_name):
    """
    Search author by name
    """
    result = vpr_request('GET', 'search?kw=%s&on=p' % author_name)
    return result


def vpr_search_module(keyword):
    result = vpr_request('GET', 'search?kw=%s&on=m&type=1' % keyword)
    return result


def voer_add_view_count(mid, version):
    if not version:
        result = vpr_request('PUT', "materials/%s/counter" % mid, {'increment': 1})
    else:
        result = vpr_request('PUT', "materials/%s/%s/counter" % (mid, version), {'increment': 1})

    return result


def vpr_get_content_file(fid):
    url = settings.VPR_URL + "mfiles/%s/get" % fid
    r = requests.request("GET", url)
    return r


def vpr_get_user_avatar(pid):
    url = settings.VPR_URL + "persons/%s/avatar" % pid
    r = requests.request("GET", url)
    return r