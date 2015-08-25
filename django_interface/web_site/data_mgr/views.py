# coding:utf8
'''
Created on 2015-02-14

@author: liliurd
'''
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import public
import utils

from exception_mgr.utils import catch_exception_http

def get_api_work_view(request):
    data = utils.get_api_work()
    return public.success_result_http(data)

def get_api_group_view(request):

    data = utils.get_api_group_list()
    return public.success_result_http(data)


def get_api_list_view(request):
    data = utils.get_api_list(request)
    return public.success_result_http(data)

@public.auth_user
def check_work_name_view(request):
    name = request.GET.get("name")
    data = utils.check_work_name(name)
    return public.success_result_http(data)

@public.auth_user
def check_structure_name_view(request):
    name = request.GET.get("name")
    data = utils.check_structure_name(name)
    return public.success_result_http(data)

@public.auth_user
def update_structure_view(request):
    data = utils.update_structure(request)
    return public.success_result_http(data)

@public.auth_user
def delete_structure_view(request):
    id = request.GET.get("id")
    data = utils.delete_structure(id)
    return public.success_result_http(data)

@public.auth_user
def update_api_view(request):
    data = utils.update_api(request)
    return public.success_result_http(data)

@public.auth_user
def delete_api_view(request):
    id = request.GET.get("id")
    data = utils.delete_api(id)
    return public.success_result_http(data)

@public.auth_user
def delete_group_view(request):
    id = request.GET.get("id")
    data = utils.delete_group(id)
    return public.success_result_http(data)

@public.auth_user
def delete_work_view(request):
    id = request.GET.get("id")
    data = utils.delete_work(id)
    return public.success_result_http(data)

def get_menu_tree_data_view(request):
    data = utils.get_menu_tree_data()
    return public.success_result_http(data)

def check_host_view(request):
    host = request.GET.get("host")
    data = utils.check_host(host)
    return public.success_result_http(data)

def filter_api_view(request):
    q = request.GET.get("q")
    data = utils.filter_api(q)
    if data:
        return public.success_result_http(data)
    else:
        return public.fail_result_http(data)

@csrf_exempt
def auto_save_api_view(request):
    data = utils.auto_save_api(request)
    return data

@public.auth_user
def copy_api_view(request):
    data = {}
    pk = request.GET.get("id")
    user = request.session.get("django_mail")
    flag = request.GET.get("flag")
    ret = utils.copy_api(pk, user, flag)
    return public.success_result_http(ret)

@public.auth_user
def delete_host_view(request):
    id = request.GET.get("id")
    ret = utils.delete_host(id)
    return public.success_result_http(ret)

@public.auth_user
def save_collection_view(request):
    ret = utils.save_collection(request)
    return public.success_result_http(ret)

@public.auth_user
def self_bench_view(request):
    ret = utils.self_bench(request)
    return public.success_result_http(ret)


def filter_group_view(request):
    work_id=request.GET.get("work_id")
    data = utils.filter_group(work_id)
    return public.success_result_http(data)

@csrf_exempt
def add_url_api_view(request):
    data = utils.add_url_api(request)
    return public.success_result_http(data)

def get_url_host_view(request):
    data = utils.get_url_host_list()
    return public.success_result_http(data)

@csrf_exempt
def set_api_badge_view(request):

    if request.method == "POST":
        body = json.loads(request.body)
        url_param = body.get("url_param")
        badge = body.get("badge")
        work = body.get("work")
        data = body.get("detail")
        ret = utils.set_api_badge(url_param, badge)
        utils.save_api_ranking(work, data)
        return public.success_result_http(ret)
    else:
        return public.fail_result_http(u"该接口为POST类型!")

def get_api_ranking_view(request):
    work = request.GET.get("work")
    data = utils.get_api_ranking_list(work)
    return public.success_result_http(data)

def user_top_ranking_view(request):
    data = utils.user_top_ranking()
    return public.success_result_http(data)

@public.auth_user
def get_api_all_version_view(request):
    id = request.GET.get("id")
    ret = utils.get_api_all_version(id)
    return public.success_result_http(ret)


@csrf_exempt
@public.auth_user
@catch_exception_http
def save_mob_version_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data["user"] = public.get_user_mail(request)
        ret = utils.save_mob_version(data)
        if ret:
            return public.fail_result_http(ret)
        return public.success_result_http(ret)
    else:
        return public.fail_result_http("Only Post!")

@catch_exception_http
def get_mob_version_list_view(request):
    ret = utils.get_mob_version_list()
    return public.success_result_http(ret)

@catch_exception_http
def get_mob_version_dict_view(request):
    id = request.GET.get("id")
    ret = utils.get_mob_version_dict(id)
    return public.success_result_http(ret)

@csrf_exempt
@public.auth_user
@catch_exception_http
def update_api_mob_version_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ret = utils.update_api_mob_version(data)
        return public.success_result_http(ret)
    else:
        return public.fail_result_http("Only Post!")

@csrf_exempt
#@public.auth_user
@catch_exception_http
def save_api_tag_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data["user"] = public.get_user_mail(request)
        ret = utils.save_api_tag(data)
        if ret:
            return public.fail_result_http(ret)
        return public.success_result_http()
    else:
        return public.fail_result_http("Only Post!")

@catch_exception_http
def get_api_tag_list_view(request):
    ret = utils.get_api_tag_list()
    return public.success_result_http(ret)

@catch_exception_http
def get_api_tag_dict_view(request):
    id = request.GET.get("id")
    ret = utils.get_api_tag_dict(id)
    return public.success_result_http(ret)

@csrf_exempt
@public.auth_user
@catch_exception_http
def bind_api_tag_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        data["user"] = public.get_user_mail(request)
        utils.bind_api_tag(data)
        return public.success_result_http()
    else:
        return public.fail_result_http("Only Post!")

@catch_exception_http
def get_tag_set_list_view(request):
    api_id = request.GET.get("api_id")
    ret = utils.get_tag_set_list(api_id)
    return public.success_result_http(ret)
