# coding:utf8
'''
Created on 2015-02-14

@author: liliurd
'''

import json
import logging
import traceback
import math
import datetime

from django.db.models import Q
import public
import models
from data_mgr import models as data_models
from data_mgr import utils as data_utils

def set_user_cookie(request):
    try:
        code = request.GET.get("code")
        if code:
            access_token_url = "%s/oauth/access_token" % public.AUTH_ROOT_URL
            statuses_url = "%s/oauth/statuses" % public.AUTH_ROOT_URL
            data = {}
            data["client_id"] = public.APP_KEY
            data["client_secret"] = public.APP_SECRET
            data["grant_type"] = "authorization_code"
            data["redirect_uri"] = public.WEB_URL
            data["code"] = code
            ret = json.loads(public.post_data(access_token_url, data))
            data = {}
            data["client_id"] = public.APP_KEY
            data["access_token"] = ret["access_token"]
            ret = json.loads(public.post_data(statuses_url, data))
            d = ret["data"]
            name = d["name"]
            mail = d["mail"]
            depart = d["depart"]
            request.session["django_name"] = name
            request.session["django_mail"] = mail
            request.session["django_depart"] = depart
            user, created = models.UserInfo.objects.get_or_create(mail=mail)
            if not created:
                user.times += 1
            else:
                user.times = 1
                user.super = 0
            works = data_models.ApiWork.objects.all()
            for work in works:
                work_id = work.id
                auth, created = models.Authorization.objects.get_or_create(user_id=user.id, work_id=work_id)
            user.name = name
            user.depart = depart
            user.options = json.dumps(d)
            user.save()
    except:
        logging.error(traceback.format_exc())


def del_user_cookie(request):
    del request.session["django_name"]
    del request.session["django_mail"]
    del request.session["django_depart"]

def get_user_info(data):

    work_id = data.get("work_id")
    flag = data.get("flag")
    q = data.get("q")

    if q:
        qset = Q(mail__icontains=q) | Q(name__icontains=q) | Q(depart__icontains=q)
        user = models.UserInfo.objects.filter(qset)
    else:
        user = models.UserInfo.objects.all()

    ret = []
    if work_id:
        work_id = int(work_id)
    for u in user:
        tmp = {}
        tmp["id"] = u.id
        tmp["mail"] = u.mail
        tmp["name"] = u.name
        tmp["depart"] = u.depart
        tmp["super"] = u.super
        auth, created = models.Authorization.objects.get_or_create(user_id=u.id, work_id=work_id)
        tmp["admin"] = auth.admin
        tmp["write"] = auth.write
        if flag == 1:
            if tmp["admin"] or tmp["super"]:
                ret.insert(0, tmp)
            else:
                ret.append(tmp)
        else:
            if tmp["admin"] or tmp["write"]:
                ret.insert(0, tmp)
            else:
                ret.append(tmp)
    page_current = data.get("page_current", 1)
    if not page_current:
        page_current = 1
    else:
        page_current = int(page_current)

    data["page"] = public.paging_algorithm(len(ret), page_current)
    if data["page"]:
        ret = ret[data["page"]["start"]:data["page"]["end"]]
    data["user_list"] = ret
    return data


def set_auth(request):
    ret = {}
    mail = request.session.get("django_mail")
    work_id = request.GET.get("work_id")
    admin = request.GET.get("admin")
    write = request.GET.get("write")
    if not work_id or not (admin or write):
        ret["code"] = public.CODE_NO
        ret["info"] = u"管理员设置输入有误，请检查输入参数！"
        return ret
    work_id = int(work_id)
    user = request.GET.get("user").strip().split("__")
    user_list = []
    for u in user:
        if u:
            user_list.append(int(u))
    auth = models.Authorization.objects.filter(work_id=work_id)
    userinfo = models.UserInfo.objects.get(mail=mail)
    if admin:
        if not userinfo.super:
            ret["code"] = public.CODE_NO
            ret["info"] = u"非超级用户不能够设置管理员！"
            return ret
        admin = int(admin)
        if admin == 1:
            auth.filter(user_id__in=user_list).update(admin=1)
        else:
            auth.filter(user_id__in=user_list).update(admin=0)
    if write:
        write = int(write)
        if write == 1:
            auth.filter(user_id__in=user_list).update(write=1)
        else:
            auth.filter(user_id__in=user_list).update(write=0)

    ret["code"] = public.CODE_OK
    ret["info"] = u"管理员设置成功！"
    return ret

def check_auth(request):
    mail = request.session.get("django_mail")
    work_id = request.GET.get("work_id", "")
    user = models.UserInfo.objects.get(mail=mail)
    ret = {}
    ret["user_id"] = user.id
    ret["work_id"] = work_id
    ret["super"] = user.super
    if work_id:
        work_id = int(work_id)
        auth, created = models.Authorization.objects.get_or_create(user_id=user.id, work_id=work_id)
        ret["admin"] = auth.admin
        ret["write"] = auth.write
    return ret

def static_user_info():
    data = {}
    user = models.UserInfo.objects.all()
    data["total"] = user.count()
    now = datetime.datetime.now()
    today = now - datetime.timedelta(days=1)
    data["day"] = user.filter(latest__gte=today).count()
    today = now - datetime.timedelta(days=7)
    data["week"] = user.filter(latest__gte=today).count()
    today = now - datetime.timedelta(days=30)
    data["month"] = user.filter(latest__gte=today).count()
    data["api_total"] = data_models.Api.objects.all().count()
    return data





