# coding:utf8
'''
Created on 2015-02-14

@author: liliurd
'''
import logging

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import json

import public
import utils
from data_mgr import utils as data_utils
import models

def redirect_login(request):
    host = request.META.get("HTTP_HOST")
    if request.GET.get("code"):
        utils.set_user_cookie(request)
        print request.GET
        redirect_url = request.GET.get("redirect_login")
        if redirect_url:
            url = redirect_url
        else:
            url = "http://" + host
        return redirect(url)

def user_logout_view(request):
    utils.del_user_cookie(request)
    host = request.META.get("HTTP_HOST")
    if host:
        url = "http://" + host
    else:
        url = public.WEB_URL
    return redirect(public.AUTH_URL+url)

@csrf_exempt
@public.auth_user
def home(request):
    data = {}
    if request.GET.get("code"):
        host = request.META.get("HTTP_HOST")
        if host:
            url = "http://" + host
        else:
            url = public.WEB_URL
        return redirect(url)
    if request.method == "GET":
        data["auth"] = utils.check_auth(request)
        data["work"] = data_utils.get_api_work()
        return render(request, 'frame.html', {"data": data})

def left_menu_view(request):
    data = {}
    data["menu"] = data_utils.get_menu_tree_data()
    return render(request, 'left_menu.html', {"data": data})

@public.auth_user
def main_view(request):
    data = {}
    data["auth"] = utils.check_auth(request)
    data["work"] = data_utils.get_api_work()
    data["user"] = utils.static_user_info()
    data["api_tag"] = data_utils.get_api_tag_count()
    rank = data_utils.user_top_ranking()
    data["user_ranking"] = {}
    user = models.UserInfo.objects.all()
    index = 0
    for r in rank:
        r["name"] = user.get(mail=r.get("user")).name
        data["user_ranking"][index] = r
        index += 1

    return render(request, 'main.html', {"data": data})

@csrf_exempt
@public.auth_user
def get_interface_view(request):
    data = {}
    data["in_q"] = request.GET.get("in_q", "")
    data["work_id"] = request.GET.get("work_id", "")
    data["group_id"] = request.GET.get("group_id", "")
    if data["work_id"]:
        data["work_id"] = int(data["work_id"])
        data["work_name"] = data_utils.get_api_work_dict(data["work_id"]).get("name")
    if data["group_id"]:
        data["group_id"] = int(data["group_id"])
        data["group_name"] = data_utils.get_api_group_dict(data["group_id"]).get("name")
    data["days"] = request.GET.get("days")
    data["o"] = request.GET.get("o")
    data["page_current"] = request.GET.get("page_current")
    data["api"] = data_utils.get_api_list(request)
    data["auth"] = utils.check_auth(request)
    return render(request, 'interface.html', {"data": data})

@csrf_exempt
@public.auth_user
def add_interface_view(request):
    if request.method == "POST":
        ret = data_utils.save_api(request)
        return public.success_result_http(ret)
    else:
        data = {}
        data["auth"] = utils.check_auth(request)
        data["work_id"] = request.GET.get("work_id", "")
        data["group_id"] = request.GET.get("group_id", "")
        data["group"] = data_utils.get_api_group_list({"work_id": data["work_id"]})
        data["work"] = data_utils.get_api_work()
        data["urlHost"] = data_utils.get_url_host_list()
        data["structure"] = data_utils.get_data_structure()
        data["api_tag"] = data_utils.get_api_tag_list()
        data["api"] = data_utils.get_api(request.GET.get("id"))
        return render(request, 'add_interface.html', {"data": data})

@public.auth_user
def interface_show_view(request):
    data = {}
    data["auth"] = utils.check_auth(request)
    data["urlHost"] = data_utils.get_url_host_list()
    data["api"] = data_utils.get_api(request.GET.get("id"))
    data["structure"] = data_utils.get_data_structure()
    data["mob_version"] = data_utils.get_mob_version_list()
    return render(request, 'interface_show.html', {"data": data})

@public.auth_user
def interface_show_api_view(request):
    data = data_utils.get_api(request.GET.get("id"))
    urlHost = data_utils.get_url_host_list()
    url_id = data.get("url")
    for url in urlHost:
        if url_id == url.get("id"):
            data["url"] = url.get("host")
    return public.success_result_http(data)
@csrf_exempt
@public.auth_user
def get_data_structure_view(request):
    data = {}
    data["structure"] = data_utils.get_data_structure()
    return render(request, 'data_structure.html', {"data": data})

@csrf_exempt
@public.auth_user
def save_data_structure_view(request):
    if request.method == "POST":
        ret = data_utils.save_data_structure(request)
        return public.success_result_http(ret)
    else:
        data = {}
        data["structure"] = data_utils.get_data_structure()
        data["current"] = data_utils.get_structure_dict(request.GET.get("id"))
        return render(request, 'edit_structure.html', {"data": data})

@public.auth_user
def get_group_view(request):
    data = {}
    data["auth"] = utils.check_auth(request)
    param = {}
    param["id"] = request.GET.get("id")
    param["work_id"] = request.GET.get("work_id", "")
    data["work_id"] = param["work_id"]
    data["group"] = data_utils.get_api_group_list(param)
    return render(request, 'api_group.html', {"data": data})

@csrf_exempt
@public.auth_user
def add_group_view(request):
    if request.method == "POST":
        data = data_utils.save_api_group(request)
        return public.success_result_http(data)
    else:
        data = {}
        data["auth"] = utils.check_auth(request)
        id = request.GET.get("id")
        data["work_id"] = request.GET.get("work_id", "")
        data["work"] = data_utils.get_api_work()
        if id:
            data["group"] = data_utils.get_api_group_dict(id)
        else:
            data["group"] = {}
        return render(request, 'add_group.html', {"data": data})

@csrf_exempt
@public.auth_user
def add_work_view(request):
    if request.method == "POST":
        data = data_utils.save_api_work(request)
        return public.success_result_http(data)
    else:
        data = {}
        data["auth"] = utils.check_auth(request)
        id = request.GET.get("id")
        if id:
            data["work"] = data_utils.get_api_work_dict(id)
        else:
            data["work"] = {}
        return render(request, 'add_work.html', {"data": data})

@csrf_exempt
@public.auth_user
def get_user_info_view(request):
    data = {}
    work_id = request.GET.get("work_id", "")
    data["work_id"] = work_id
    data["q"] = request.GET.get("q", "")
    data["flag"] = public.ADMIN_FLAG
    data["page_current"] = request.GET.get("page_current")
    data["user"] = utils.get_user_info(data)
    data["auth"] = utils.check_auth(request)
    return render(request, 'set_admin.html', {"data": data})

@csrf_exempt
@public.auth_user
def get_write_user_info_view(request):
    data = {}
    work_id = request.GET.get("work_id", "")
    data["work_id"] = work_id
    data["q"] = request.GET.get("q", "")
    data["flag"] = public.WRITE_FLAG
    data["page_current"] = request.GET.get("page_current")
    data["user"] = utils.get_user_info(data)
    data["auth"] = utils.check_auth(request)
    return render(request, 'set_write.html', {"data": data})

@public.auth_user
def set_auth_view(request):
    data = utils.set_auth(request)
    return public.success_result_http(data)

@public.auth_user
def get_url_host_list_view(request):
    data = {}
    data["host"] = data_utils.get_url_host_list()
    return render(request, 'url_host.html', {"data": data})

@csrf_exempt
@public.auth_user
def edit_url_host_view(request):
    if request.method == "POST":
        ret = data_utils.edit_host(request)
        return public.success_result_http(ret)
    else:
        data = {}
        id = request.GET.get("id")
        data["host"] = data_utils.get_url_host_dict(id)
        return render(request, 'edit_host.html', {"data": data})

@public.auth_user
def self_bench_view(request):
    data = data_utils.self_bench(request)
    return render(request, 'self_bench.html', {"data": data})

@public.auth_user
def api_ranking_view(request):
    work = request.GET.get("work")
    data = data_utils.get_api_ranking_list(work)
    return render(request, 'api_ranking.html', {"data": data})

def help_view(request):
    return render(request, 'help.html')

@public.auth_user
def query_api_view(request):
    mob_version_id = request.GET.get("mob_version_id")
    tag_id = request.GET.get("tag_id")
    if mob_version_id:
        data = data_utils.query_mob_version_api(mob_version_id)
    elif tag_id:
        data = data_utils.query_tag_api(tag_id)
    else:
        data = []
    return render(request, 'interface_mob.html', {"data": data})
