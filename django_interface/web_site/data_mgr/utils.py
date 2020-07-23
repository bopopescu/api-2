# coding:utf8
'''
Created on 2015-02-14

@author: liliurd
'''

import json
import math
import datetime
import logging
from django.db.models import Q
from django.db.models import Count
from urlparse import urlparse
from django.forms.models import model_to_dict
import models
import public
from web_mgr import models as web_models


def get_api_work():
    '''
    获取所有业务信息
    '''
    apiWorks = models.ApiWork.objects.all().order_by("id")
    apiGroups = models.ApiGroup.objects.all()
    api = models.Api.objects.all()
    data = []
    for work in apiWorks:
        tmp = model_to_dict(work)
        group = apiGroups.filter(work_id=tmp["id"])
        id_list = []
        for g in group:
            id_list.append(g.id)
        api_list = api.filter(group_id__in=id_list)
        tmp["api_num"] = api_list.count()
        tmp["group_num"] = len(id_list)

        now = datetime.datetime.now()
        pre_week = now - datetime.timedelta(days=7)
        pre_month = now - datetime.timedelta(days=30)
        tmp["api_week"] = api_list.filter(modify__gte=pre_week).count()
        tmp["api_month"] = api_list.filter(modify__gte=pre_month).count()
        data.append(tmp)
    return data


def get_api_work_dict(id):
    '''
    获取当个业务信息
    :param id:
    :return:
    '''
    work = models.ApiWork.objects.get(id=id)
    ret = model_to_dict(work)
    ret["is_show"] = int(work.is_show)
    return ret


def check_work_name(name):
    data = {}
    if name:
        num = models.ApiWork.objects.filter(name=name).count()
    else:
        num = -1
    if num > 0:
        data["code"] = public.CODE_NO
        data["info"] = u"该检查项已经存在，继续使用会覆盖原数据！"
    elif num == -1:
        data["code"] = public.CODE_NO
        data["info"] = u"请先输入检查项！"
    else:
        data["code"] = public.CODE_OK
        data["info"] = u"该检查项无重复，可以使用！"
    return data


def save_api_work(request):
    '''
    保存业务信息
    :param request:
    :return:
    '''
    ret = {}
    data = json.loads(request.body)
    if not data.get("name"):
        ret["code"] = public.CODE_NO
        ret["info"] = u"请输入业务名称！"
        return ret
    work, created = models.ApiWork.objects.get_or_create(name=data.get("name"))
    work.name = data.get("name")
    work.description = data.get("description")
    work.is_show = int(data.get("is_show"))
    work.user = request.session.get("django_mail")
    work.save()
    ret["code"] = public.CODE_OK
    return ret


def delete_work(id):
    '''
    删除业务
    :param id:
    :return:
    '''
    data = {}
    if id:
        id = int(id)
        group = models.ApiGroup.objects.filter(work_id=id).count()
        if group > 0:
            data["code"] = public.CODE_NO
            data["info"] = u"该业务下面包含分组，请先删除分组！"
            return data
        work = models.ApiWork.objects.filter(id=id)
        if work:
            web_models.Authorization.objects.filter(work_id=id).delete()
            work.delete()

    data["code"] = public.CODE_OK
    return data


def get_api_group_list(data={}):
    '''
    获取所有分组信息
    :param data:
    :return:
    '''
    id = data.get("id")
    work_id = data.get("work_id")
    if work_id:
        work_id = int(work_id)
        apiGroup = models.ApiGroup.objects.filter(work_id=work_id)
    else:
        apiGroup = models.ApiGroup.objects.all()
    if id:
        apiGroup = apiGroup.filter(id=id)
    data = []
    for api in apiGroup:
        tmp = model_to_dict(api)
        tmp["is_show"] = int(api.is_show)
        data.append(tmp)
    return data


def get_api_group_dict(id):
    '''
    获取单个分组信息
    :param id:
    :return:
    '''
    ret = {}
    if id:
        group = models.ApiGroup.objects.get(id=id)
        ret = model_to_dict(group)
        ret["is_show"] = int(group.is_show)
    return ret


def save_api_group(request):
    '''
    保存分组信息
    :param request:
    :return:
    '''
    ret = {}
    data = json.loads(request.body)
    name = data.get("name")
    work_id = data.get("work_id")
    if not name:
        ret["code"] = public.CODE_NO
        ret["info"] = u"请输入分组名称！"
        return ret
    id = data.get("id")
    if id:
        count = models.ApiGroup.objects.filter(work_id=work_id, name=name).exclude(id=id).count()
    else:
        count = models.ApiGroup.objects.filter(work_id=work_id, name=name).count()
    if count:
        ret["code"] = public.CODE_NO
        ret["info"] = u"该分组名在业务中已存在！"
        return ret

    if id:
        group = models.ApiGroup.objects.get(id=int(id))
    else:
        group = models.ApiGroup()
    group.name = name
    group.work_id = work_id
    group.is_show = int(data.get("is_show"))
    group.description = data.get("description")
    group.user = request.session.get("django_mail")
    group.save()

    ret["code"] = public.CODE_OK
    return ret


def delete_group(id):
    '''
    删除分组
    :param id:
    :return:
    '''
    data = {}
    if id:
        id = int(id)
        api = models.Api.objects.filter(group_id=id).count()
        if api > 0:
            data["code"] = public.CODE_NO
            data["info"] = u"该分组下面包含接口，请先删除接口！"
            return data
        group = models.ApiGroup.objects.filter(id=id)
        if group:
            group.delete()

    data["code"] = public.CODE_OK
    return data


def get_api_list(request):
    '''
    获取所有接口信息
    :param request:
    :return:
    '''
    q = request.GET.get("q", "")
    if q.startswith("/"):
        q1 = q[1:]
    else:
        q1 = "/" + q
    in_q = request.GET.get("in_q", "")
    if in_q.startswith("/"):
        in_q1 = in_q[1:]
    else:
        in_q1 = "/" + in_q
    work_id = request.GET.get("work_id", "")
    group_id = request.GET.get("group_id", "")
    page_current = request.GET.get("page_current")
    days = request.GET.get("days")
    o = request.GET.get("o")
    user = request.session.get("django_mail")

    if not page_current:
        page_current = 1
    else:
        page_current = int(page_current)
    qset = None
    if q:
        qset = Q(name__icontains=q) | Q(url_param__icontains=q) | Q(url_param__icontains=q1) | Q(user__icontains=q)
    elif in_q:
        qset = Q(name__icontains=in_q) | Q(url_param__icontains=in_q) | Q(url_param__icontains=in_q1) | Q(
            user__icontains=in_q)
    if qset:
        api = models.Api.objects.filter(qset)
    else:
        api = models.Api.objects.all()
    group_list = []
    if work_id:
        group = models.ApiGroup.objects.filter(work_id=work_id)
    else:
        group = models.ApiGroup.objects.all()
    for g in group:
        group_list.append(g.id)

    if group_list:
        if not group_id:
            api = api.filter(group_id__in=group_list)
        elif int(group_id) in group_list:
            api = api.filter(group_id=group_id)
        else:
            api = []
    else:
        api = []
    if days:
        days = int(days)
        now = datetime.datetime.now()
        days = now - datetime.timedelta(days=days)
        if api:
            api = api.filter(modify__gte=days)
    if api:
        if o:
            api = api.order_by(o)
        else:
            api = api.order_by("-id")
    data = {}
    data["page"] = public.paging_algorithm(len(api), page_current)
    if data["page"]:
        api = api[data["page"]["start"]:data["page"]["end"]]

    data["api_list"] = []
    collection = models.ApiCollection.objects.filter(user=user)
    for a in api:
        tmp = {}
        tmp["id"] = a.id
        tmp["collection"] = collection.filter(api_id=tmp["id"])
        tmp["group_id"] = a.group_id
        tmp["group"] = get_api_group_dict(tmp["group_id"])
        tmp["work"] = get_api_work_dict(tmp["group"]["work_id"])
        tmp["name"] = a.name
        tmp["url"] = a.url
        tmp["url_param"] = a.url_param
        tmp["status"] = int(a.status)
        tmp["request_type"] = int(a.request_type)
        tmp["is_show"] = a.is_show
        tmp["version"] = a.version
        tmp["user"] = a.user
        tmp["badge"] = a.badge
        if tmp["user"]:
            tmp["user_name"] = a.user.split("@")[0]
        else:
            tmp["user_name"] = ""
        data["api_list"].append(tmp)
    return data


def get_api(id):
    '''
    获取指定接口信息
    :param id:
    :return:
    '''
    ret = {}
    if id:
        api = models.Api.objects.get(id=id)
        ret["id"] = api.id
        ret["group_id"] = int(api.group_id)
        ret["work_id"] = int(get_api_group_dict(ret["group_id"]).get("work_id"))
        ret["name"] = api.name
        ret["url"] = int(api.url)
        ret["url_param"] = api.url_param
        ret["user"] = api.user
        ret["user_name"] = api.user.split("@")[0]
        ret["status"] = int(api.status)
        ret["request_type"] = int(api.request_type)
        ret["is_show"] = int(api.is_show)
        ret["version"] = api.version
        ret["mob_version_id"] = api.mob_version_id
        ret["description"] = api.description
        ret["in_param"] = json.loads(api.in_param) if api.in_param else []
        ret["out_param"] = json.loads(api.out_param) if api.out_param else []
        ret["ret_param"] = api.ret_param
        ret["options"] = api.options
        ret["error_param"] = json.loads(api.error_param) if api.error_param else []
        ret["group"] = get_api_group_dict(ret["group_id"])
        ret["work"] = get_api_work_dict(ret["group"]["work_id"])
        ret["api_tag_list"] = get_tag_set_list(api.id)
    return ret


def save_api(request):
    '''
    保存接口信息
    :param request:
    :return:
    '''
    data = json.loads(request.body)
    ret_param = data.get("ret_param")
    options = data.get("options")
    tag_id_list = data.get("tag_id_list")
    print tag_id_list
    # if ret_param:
    #    try:
    #        eval(ret_param)
    #    except:
    #        data["code"] = public.CODE_NO
    #        data["info"] = u"返回值不是一个合法的JSON字符串!"
    #        return data
    #else:
    #    ret_param = "{}"
    user = request.session.get("django_mail")
    base = data.get("base", {})
    if base.get("url") == "0":
        data["code"] = public.CODE_NO
        data["info"] = u"请先选择主站域名!"
        return data
    group_id = base.get("group_id")
    if not group_id:
        work_id = base.get("work_id")
        if not work_id:
            data["code"] = public.CODE_NO
            data["info"] = u"请先选择所属分组!"
            return data
        else:
            groups = models.ApiGroup.objects.filter(work_id=work_id)
            if len(groups):
                group_id = groups[0].id
            else:
                groups = models.ApiGroup()
                groups.work_id = int(work_id)
                groups.name = u"默认分组"
                groups.is_show = True
                groups.user = "liliurd@meilishuo.com"
                groups.description = "自动添加"
                groups.save()
                group_id = groups.id

    group_id = int(group_id)
    group = models.ApiGroup.objects.get(id=group_id)
    work_id = group.work_id
    userInfo = web_models.UserInfo.objects.get(mail=user)
    user_id = userInfo.id
    super = userInfo.super
    if not super:
        num = web_models.Authorization.objects.filter(user_id=user_id, work_id=work_id).filter(
            Q(admin=1) | Q(write=1)).count()
        if num == 0:
            data["code"] = public.CODE_NO
            data["info"] = u"您对所选的业务没有写权限，保存接口失败!"
            return data

    inputJson = data.get("inputJson", [])
    inputList = []
    # 名称::类型::是否必须::示例值::描述
    tmp = {}
    for d in inputJson:
        tmpList = d.strip().split("::")
        if len(tmpList) == 5:
            name = tmpList[0]
            tmp_dict = {"name": name, "type": int(tmpList[1]), "must": int(tmpList[2]), "sample": tmpList[3],
                        "desc": tmpList[4]}
            if name not in tmp:
                inputList.append(tmp_dict)
            tmp[name] = tmp_dict
    outputJson = data.get("outputJson", [])
    outputList = []
    #名称::内部参数名称::类型::示例值::描述
    tmp = {}
    for d in outputJson:
        tmpList = d.strip().split("::")
        if len(tmpList) == 4:
            name = tmpList[0]
            tmp_dict = {"name": name, "type": int(tmpList[1]), "sample": tmpList[2],
                        "desc": tmpList[3]}
            if name not in tmp:
                outputList.append(tmp_dict)
            tmp[name] = tmp_dict

    errorJson = data.get("errorJson", [])
    errorList = []
    #错误码::内部错误码::解决方案::描述
    tmp = {}
    for d in errorJson:
        tmpList = d.strip().split("::")
        if len(tmpList) == 3:
            name = tmpList[0]
            tmp_dict = {"code": name, "solve": tmpList[1], "desc": tmpList[2]}
            if name not in tmp:
                errorList.append(tmp_dict)
            tmp[name] = tmp_dict

    if base.get("id"):
        api = models.Api.objects.get(id=base.get("id"))
    else:
        api, created = models.Api.objects.get_or_create(url=base.get("url"), url_param=base.get("url_param"))
    api.group_id = group_id
    api.name = base.get("name")
    api.url = base.get("url")
    api.url_param = base.get("url_param")
    api.request_type = base.get("request_type")
    api.status = base.get("status")
    api.is_show = int(base.get("is_show"))
    api.version = base.get("version")
    api.description = base.get("description")
    api.user = request.session.get("django_mail")
    api.in_param = json.dumps(inputList)
    api.out_param = json.dumps(outputList)
    api.ret_param = ret_param
    api.options = options
    api.error_param = json.dumps(errorList)
    api.save()

    bind_api_tag({"api_id": api.id, "tag_id_list": tag_id_list})
    data["code"] = public.CODE_OK
    return data


def update_api(request):
    '''
    更改接口状态
    :param request:
    :return:
    '''
    id = request.GET.get("id")
    status = request.GET.get("status")
    data = {}
    if id and status:
        id = int(id)
        models.Api.objects.filter(id=id).update(status=status)
    data["code"] = public.CODE_OK
    return data


def delete_api(id):
    '''
    删除接口
    :param id:
    :return:
    '''
    if id:
        api = models.Api.objects.filter(id=id)
        if api:
            api_subordinate = models.Api.objects.filter(subordinate_api=id).order_by("id")
            if api_subordinate:
                subordinate_id = api_subordinate[0].id
                api_subordinate.update(subordinate_api=subordinate_id)
                models.Api.objects.filter(id=subordinate_id).update(subordinate_api=0)
            api.delete()
    data = {}
    data["code"] = public.CODE_OK
    return data


def get_data_structure():
    '''
    获取所有数据结构信息
    :return:
    '''
    data = models.DataStructure.objects.all()
    ret = []
    for d in data:
        tmp = model_to_dict(d)
        tmp["detail"] = json.loads(d.detail)
        ret.append(tmp)
    return ret


def get_structure_dict(id):
    '''
    获取指定数据结构信息
    :param id:
    :return:
    '''
    ret = {}
    if id:
        data = models.DataStructure.objects.get(id=id)
        ret = model_to_dict(data)
        ret["detail"] = json.loads(data.detail)
    return ret


def check_structure_name(name):
    '''
    检查数据结构名是否存在
    :param name:
    :return:
    '''
    data = {}
    if name:
        num = models.DataStructure.objects.filter(name=name).count()
    else:
        num = -1
    if num > 0:
        data["code"] = public.CODE_NO
        data["info"] = u"该检查项已经存在，继续使用会覆盖原数据！"
    elif num == -1:
        data["code"] = public.CODE_NO
        data["info"] = u"请先输入检查项！"
    else:
        data["code"] = public.CODE_OK
        data["info"] = u"该检查项无重复，可以使用！"
    return data


def save_data_structure(request):
    '''
    保存数据结构信息
    :param request:
    :return:
    '''
    data = json.loads(request.body)
    base = data.get("base", {})

    if not base.get("name"):
        data["code"] = public.CODE_NO
        data["info"] = u"数据结构名不能为空!"
        return data

    inputJson = data.get("inputJson", {})
    inputList = []
    # 名称::类型::示例值::描述
    tmp = {}
    for d in inputJson:
        tmpList = d.strip().split("::")
        if len(tmpList) == 4:
            name = tmpList[0]
            tmp[name] = {"name": name}
            tmp[name]["type"] = int(tmpList[1])
            tmp[name]["sample"] = tmpList[2]
            tmp[name]["desc"] = tmpList[3]
    for t in tmp:
        inputList.append(tmp[t])

    api, created = models.DataStructure.objects.get_or_create(name=base.get("name"))
    api.name = base.get("name")
    api.description = base.get("description")
    api.is_base = False
    api.user = request.session.get("django_mail")
    api.detail = json.dumps(inputList)
    api.save()

    data["code"] = public.CODE_OK
    return data


def update_structure(request):
    '''
    更改数据结构状态
    :param request:
    :return:
    '''
    s_id = request.GET.get("id")
    status = request.GET.get("status")
    data = {}
    if s_id and status:
        s_id = int(s_id)
        models.DataStructure.objects.filter(id=s_id).update(status=status)
    data["code"] = public.CODE_OK
    return data


def delete_structure(id):
    '''
    删除数据结构
    :param id:
    :return:
    '''
    if id:
        id = int(id)
        api = models.DataStructure.objects.filter(id=id)
        if api:
            api.delete()
    data = {}
    data["code"] = public.CODE_OK
    return data


def get_all_count():
    ret = {}
    work = models.ApiWork.objects.all()
    group = models.ApiGroup.objects.all()
    api = models.Api.objects.all()
    structure = models.DataStructure.objects.all()
    ret["work"] = work.count()
    ret["group"] = group.count()
    ret["api"] = api.count()
    ret["api_release"] = api.filter(status="1").count()
    ret["api_not_release"] = ret["api"] - ret["api_release"]
    ret["structure"] = structure.count()
    ret["structure_release"] = structure.filter(status="1").count()
    ret["structure_not_release"] = ret["structure"] - ret["structure_release"]

    return ret


def get_menu_tree_data():
    '''
    获取左侧菜单树信息
    :return:
    '''
    works = models.ApiWork.objects.all().order_by("id")
    groups = models.ApiGroup.objects.all()
    data = []
    for work in works:
        tmp_work = {}
        tmp_work["id"] = work.id
        tmp_work["name"] = work.name
        tmp_work["group"] = []
        groups_tmp = groups.filter(work_id=tmp_work["id"])
        # total = 0
        for group in groups_tmp:
            tmp_group = {}
            tmp_group["id"] = group.id
            tmp_group["name"] = group.name
            tmp_group["work_id"] = tmp_work["id"]
            tmp_group["api_num"] = models.Api.objects.filter(group_id=tmp_group["id"]).count()
            tmp_work["group"].append(tmp_group)
            #total += tmp_group["api_num"]
        #tmp_work["api_num"] = total
        tmp_work["api_num"] = len(groups_tmp)
        data.append(tmp_work)
    return data


def get_url_host_list():
    '''
    获取所有域名信息
    :return:
    '''
    urlHost = models.UrlHost.objects.all().order_by("host")
    ret = []
    for host in urlHost:
        tmp = model_to_dict(host)
        ret.append(tmp)
    return ret


def get_url_host_dict(id):
    ret = {}
    if id:
        urlHost = models.UrlHost.objects.get(id=id)
        ret = model_to_dict(urlHost)
    return ret


def check_host(host):
    '''
    检查域名是否存在
    :param host:
    :return:
    '''
    data = {}
    if not host:
        data["code"] = public.CODE_NO
        data["info"] = u"请先输入需要检测的域名！"
        return data
    if host.endswith("/"):
        host = host[:-1]
    num = models.UrlHost.objects.filter(host=host).count()
    if num > 0:
        data["code"] = public.CODE_NO
        data["info"] = u"该域名已经存在，继续保存会覆盖原数据！"
    else:
        data["code"] = public.CODE_OK
        data["info"] = u"该域名可用，没有重复项！"
    return data


def edit_host(request):
    '''
    编辑域名
    :param request:
    :return:
    '''
    data = {}
    body = json.loads(request.body)
    host = body.get("host")
    if host.endswith("/"):
        host = host[:-1]
    id = body.get("id")
    if not host:
        data["code"] = public.CODE_NO
        data["info"] = u"域名不能为空！"
        return data
    if id:
        id = int(id)
        urlHost = models.UrlHost.objects.get(id=id)
    else:
        urlHost = models.UrlHost()
        if models.UrlHost.objects.filter(host=host).count():
            data["code"] = public.CODE_NO
            data["info"] = u"域名已经存在，请直接使用或者重新输入域名！"
            return data
    urlHost.host = host
    urlHost.description = body.get("description")
    urlHost.user = request.session.get("django_mail")
    urlHost.save()
    data["code"] = public.CODE_OK
    return data


def filter_api(q):
    ret = []
    if q:
        apis = models.Api.objects.filter(url_param=q)
        for api in apis:
            tmp = {}
            tmp["id"] = api.id
            tmp["name"] = api.name
            group = get_api_group_dict(api.group_id)
            work_id = group.get("work_id")
            tmp["group_name"] = group.get("name")
            tmp["work_name"] = get_api_work_dict(work_id).get("name")
            tmp["name"] = api.name
            tmp["url"] = get_url_host_dict(api.url).get("host")
            tmp["url_param"] = api.url_param
            tmp["request_type"] = int(api.request_type)
            tmp["description"] = api.description
            tmp["in_param"] = json.loads(api.in_param)
            tmp["out_param"] = json.loads(api.out_param)
            tmp["error_param"] = json.loads(api.error_param)
            tmp["ret_param"] = api.ret_param
            tmp["options"] = api.options
            ret.append(tmp)
    return ret


# 配合脚本自动保存api接口
def auto_save_api(request):
    ret = []
    data = json.loads(request.body)
    group_id = data.get("group_id")
    if not group_id:
        return ret
    api = models.Api()
    api.group_id = int(group_id)
    api.name = data.get("name")
    api.url = data.get("url")
    api.url_param = data.get("url_param")
    api.status = data.get("status")
    api.request_type = data.get("request_type")
    api.user = data.get("user")
    api.version = ""
    api.description = data.get("description")
    api.ret_param = data.get("ret_param", "")
    api.in_param = json.dumps(data.get("in_param", []))
    api.out_param = json.dumps(data.get("out_param", []))
    api.error_param = json.dumps(data.get("error_param", []))
    api.save()

    return data


def copy_api(pk, user="", flag=None):
    data = {}
    if pk:
        api = models.Api.objects.get(id=pk)
        if not flag:
            subordinate_api = api.subordinate_api
            if not subordinate_api:
                subordinate_api = api.id
            api.subordinate_api = subordinate_api
        else:
            api.subordinate_api = 0
        api.id = None
        if user:
            api.user = user
        api.save()
        data["code"] = public.CODE_OK
    else:
        data["code"] = public.CODE_NO
        data["info"] = u"更新版本的接口不存在！"
    return data


def delete_host(id):
    data = {}
    if id:
        num = models.Api.objects.filter(url=id).count()
        if num:
            data["code"] = public.CODE_NO
            data["info"] = u"有接口正在使用该域名，请先删除相关接口！"
            return data
        models.UrlHost.objects.filter(id=id).delete()
    data["code"] = public.CODE_OK
    return data


def save_collection(request):
    data = {}
    data["code"] = public.CODE_OK
    user = request.session.get("django_mail")
    api_id = request.GET.get("api_id")
    if api_id and user:
        collection = models.ApiCollection.objects.filter(user=user, api_id=api_id)
        if collection.count():
            collection.delete()
            data["info"] = u"去掉接口收藏成功！"
        else:
            models.ApiCollection.objects.get_or_create(user=user, api_id=api_id)
            data["info"] = u"接口收藏成功，请在个人工作台中查看！"
    return data


def self_bench(request):
    django_mail = request.session.get("django_mail")
    user = web_models.UserInfo.objects.get(mail=django_mail)
    user_id = user.id
    is_super = user.super
    auth = web_models.Authorization.objects.filter(user_id=user_id)
    work = models.ApiWork.objects.all()
    admin = auth.filter(admin=1)
    write = auth.filter(Q(write=1) | Q(admin=1))
    data = {}
    data["super"] = is_super
    data["admin"] = []
    data["write"] = []
    data["collection"] = []
    for a in admin:
        tmp = {}
        tmp["id"] = a.work_id
        tmp["name"] = work.get(id=tmp["id"]).name
        data["admin"].append(tmp)
    work_list = []
    for a in write:
        tmp = {}
        tmp["id"] = a.work_id
        tmp["name"] = work.get(id=tmp["id"]).name
        data["write"].append(tmp)
        work_list.append(tmp["id"])
    collection = models.ApiCollection.objects.filter(user=django_mail)
    for a in collection:
        tmp = get_api(a.api_id)
        if tmp:
            #如果接口不可见，则只有超级用户和可写权限的人显示
            if is_super or tmp.get("is_show") or tmp.get("work_id") in work_list:
                data["collection"].append(tmp)
    return data


def filter_group(work_id):
    data = []
    if work_id:
        work_id = int(work_id)
        group = models.ApiGroup.objects.filter(work_id=work_id)
        for g in group:
            tmp = {}
            tmp["id"] = g.id
            tmp["name"] = g.name
            tmp["work_id"] = work_id
            data.append(tmp)
    return data


def add_url_api(request):
    body = json.loads(request.body)
    urls = body.get("url")
    data = {}
    if not urls:
        data["code"] = public.CODE_NO
        data["info"] = u"请先输入URL列表值！"
        return data
    url_list = urls.strip().split("\n");
    err_url = ""
    err_host = ""
    url_check = []
    for url in url_list:
        u = urlparse(url)
        path = u.path
        scheme = u.scheme
        netloc = u.netloc
        if not path or not scheme or not netloc:
            err_url += url + "\n"
        host = "%s://%s" % (scheme, netloc)
        if host.endswith("/"):
            host1 = host[:-1]
        else:
            host1 = host + "/"
        qset = Q(host=host) | Q(host=host1)
        url_mun = models.UrlHost.objects.filter(qset).count()
        if url_mun == 0:
            err_host += host + "\n"

    if err_url:
        data["code"] = public.CODE_NO
        data["info"] = u"接口保存失败, 存在无法识别URL：\n" + err_url
        return data;
    if err_host:
        data["code"] = public.CODE_NO
        data["info"] = u"接口保存失败, 主站域名不存在，请在域名管理中添加或者使用已有线上域名：\n" + err_host
        return data;

    for url in url_list:
        u = urlparse(url)
        path = u.path
        scheme = u.scheme
        netloc = u.netloc
        querys = u.query.strip().split("&")
        host = "%s://%s" % (scheme, netloc)
        if host.endswith("/"):
            host1 = host[:-1]
        else:
            host1 = host + "/"
        qset = Q(host=host) | Q(host=host1)
        url_mod = models.UrlHost.objects.filter(qset)
        if len(url_mod):
            url_id = url_mod[0].id
        else:
            urlhost = models.UrlHost()
            urlhost.host = host
            urlhost.user = request.session.get("django_mail")
            urlhost.save()
            url_id = urlhost.id

        in_data = []
        for query in querys:
            q = query.strip().split("=")
            if len(q) == 2:
                tmp = {}
                tmp["name"] = q[0];
                tmp["sample"] = q[1];
                tmp["must"] = 1;
                tmp["desc"] = "";
                try:
                    tmp["sample"] = int(tmp["sample"])
                    tmp["type"] = 1
                except:
                    tmp["type"] = 3
                in_data.append(tmp)
        group_id = body.get("group_id")
        if not group_id:
            work_id = body.get("work_id")
            if not work_id:
                data["code"] = public.CODE_NO
                data["info"] = u"请先选择所属分组!"
                return data
            else:
                groups = models.ApiGroup.objects.filter(work_id=work_id)
                if len(groups):
                    group_id = groups[0].id
                else:
                    groups = models.ApiGroup()
                    groups.work_id = int(work_id)
                    groups.name = u"默认分组"
                    groups.is_show = True
                    groups.user = "liliurd@meilishuo.com"
                    groups.description = "自动添加"
                    groups.save()
                    group_id = groups.id
        api = models.Api()
        api.group_id = group_id
        api.name = u"待确认的接口"
        api.url = url_id
        api.url_param = path
        api.status = 0
        api.request_type = 1
        api.is_show = 1
        api.user = request.session.get("django_mail")
        api.description = ""
        api.in_param = json.dumps(in_data)
        api.out_param = json.dumps([])
        api.error_param = json.dumps([])
        api.ret_param = ""
        api.options = url
        api.save()

    data["code"] = public.CODE_OK
    data["info"] = u"接口保存成功，请再次确认已经生成接口信息！"
    return data;


def set_api_badge(url_param, badge):
    if not isinstance(url_param, list):
        url_param = [url_param]
    badge = int(badge)
    ret = models.Api.objects.filter(url_param__in=url_param).update(badge=badge)
    return ret


def save_api_ranking(work, data):
    if work and data:
        models.ApiRanking.objects.filter(work=work).delete()
        for d in data:
            path = d.get("path")
            total = d.get("total")
            if path and total:
                total = int(total)
                rank = models.ApiRanking()
                rank.work = work
                rank.path = path
                rank.total = total
                rank.save()


def get_api_ranking_list(work=None):
    if work:
        ranks = models.ApiRanking.objects.filter(work=work).order_by("-total")
    else:
        ranks = models.ApiRanking.objects.all().order_by("-total")
    data = []
    for rank in ranks:
        tmp = model_to_dict(rank)
        data.append(tmp)
    return data


def user_top_ranking():
    data = list(models.Api.objects.values('user').annotate(count=Count('user')).order_by("-count"))[0:10]
    return data


def get_api_all_version(id):
    api = models.Api.objects.get(id=id)
    subordinate_api = api.subordinate_api
    ret = []
    if not subordinate_api:
        subordinate_api = api.id
        source_api = api
    else:
        source_api = models.Api.objects.get(id=subordinate_api)
    tmp = {}
    tmp["id"] = source_api.id
    tmp["name"] = source_api.name
    tmp["url_param"] = source_api.url_param
    tmp["user"] = source_api.user
    tmp["version"] = source_api.version
    tmp["create"] = public.datetime2str(source_api.create)
    ret.append(tmp)
    api_list = models.Api.objects.filter(subordinate_api=subordinate_api)
    for a in api_list:
        tmp = {}
        tmp["id"] = a.id
        tmp["name"] = a.name
        tmp["url_param"] = a.url_param
        tmp["user"] = a.user
        tmp["version"] = a.version
        tmp["create"] = public.datetime2str(a.create)
        ret.append(tmp)
    return ret


def save_mob_version(data):
    if data.get("name"):
        mob, create = models.MobVersion.objects.get_or_create(name=data.get("name"))
        mob.description = data.get("description")
        mob.user = data.get("user")
        mob.save()
        return None
    else:
        return u"版本名不能为空"


def get_mob_version_list():
    mob = models.MobVersion.objects.all()
    ret = []
    for m in mob:
        tmp = {}
        tmp["id"] = m.id
        tmp["name"] = m.name
        tmp["user"] = m.user
        tmp["description"] = m.description
        ret.append(tmp)
    return ret


def get_mob_version_dict(id):
    mob = models.MobVersion.objects.get(id=id)
    ret = model_to_dict(mob)
    return ret


def update_api_mob_version(data):
    api_id = data.get("api_id")
    mob_version_id = data.get("mob_version_id")
    models.Api.objects.filter(id=api_id).update(mob_version_id=mob_version_id)


def query_mob_version_api(mob_version_id):
    api = models.Api.objects.filter(mob_version_id=mob_version_id)
    ret = []
    for d in api:
        tmp = {}
        tmp["id"] = d.id
        tmp["name"] = d.name
        tmp["url_param"] = d.url_param
        tmp["user"] = d.user
        tmp["request_type"] = int(d.request_type)
        tmp["user"] = int(d.status)
        tmp["user_name"] = d.user.split("@")[0] if d.user else ""
        tmp["badge"] = d.badge
        ret.append(tmp)
    return ret

def save_api_tag(data):
    name = data.get("name")
    if not name:
        return u"标签名不能为空"
    data["name"] = name[:8]
    tag, create = models.ApiTags.objects.get_or_create(name=data["name"])
    public.Model(tag).save_unique(data)

def bind_api_tag(data):
    api_id = data.get("api_id")
    tag_id_list = data.get("tag_id_list")
    if not isinstance(tag_id_list, list):
        tag_id_list = [tag_id_list]
    models.ApiTagsSet.objects.filter(api_id=api_id).delete()
    for tag_id in tag_id_list:
        models.ApiTagsSet.objects.get_or_create(api_id=api_id, tag_id=tag_id)

def get_api_tag_list():
    tag = models.ApiTags.objects.all()
    return public.Model(tag).get_list()

def get_api_tag_dict(id):
    tag = models.ApiTags.objects.get(id=id)
    return public.Model(tag).get_dict()

def get_tag_set_list(api_id):
    tag_set = models.ApiTagsSet.objects.filter(api_id=api_id)
    tags = public.Model(tag_set).get_list()
    ret = []
    for tag in tags:
        try:
            t = models.ApiTags.objects.get(id=tag.get("tag_id"))
            ret.append(public.Model(t).get_dict())
        except:
            pass
    return ret

def get_api_tag_count():
    data = get_api_tag_list()
    tag_set = models.ApiTagsSet.objects.all()
    ret = []
    for d in data:
        d["api_num"] = tag_set.filter(tag_id=d["id"]).count()
        ret.append(d)
    return ret

def query_tag_api(tag_id):
    tag_set = models.ApiTagsSet.objects.filter(tag_id=tag_id)
    id_list = []
    for d in tag_set:
        id_list.append(d.api_id)
    api = models.Api.objects.filter(id__in=id_list)
    ret = []
    for d in api:
        tmp = {}
        tmp["id"] = d.id
        tmp["name"] = d.name
        tmp["url_param"] = d.url_param
        tmp["version"] = d.version
        tmp["user"] = d.user
        tmp["request_type"] = int(d.request_type)
        tmp["user"] = int(d.status)
        tmp["user_name"] = d.user.split("@")[0] if d.user else ""
        tmp["badge"] = d.badge
        ret.append(tmp)
    return ret











