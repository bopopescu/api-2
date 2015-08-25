# coding:utf-8
import datetime
import time
import traceback
import json
import functools
import urllib
import urllib2
import math

from django.http import HttpResponse
from django.shortcuts import redirect
from django.forms.models import model_to_dict

AUTH_ROOT_URL = "http://api.speed.meilishuo.com"
APP_KEY = "100055"
APP_SECRET = "60f543fe273eb6e7a137b5041741491a"

WEB_URL = "http://interfaces.meiliworks.com/"
AUTH_URL = "%s/oauth/authorize?client_id=%s&response_type=code&redirect_uri=" % (AUTH_ROOT_URL, APP_KEY)
REDIRECT_URL = "/redirect_login?redirect_login="

LOWER_STATUS_FAIL = "fail"
LOWER_STATUS_SUCCESS = "success"

CODE_OK = 0
CODE_NO = 1
#每页显示记录条数
PAGING_NUM = 50
#显示最大分页数
MAX_PAGING = 11

#用户权限标识
ADMIN_FLAG = 1
WRITE_FLAG = 2

#api参数类型
PARAMS_TYPE_INPUT = 1
PARAMS_TYPE_OUTPUT = 2
PARAMS_TYPE_ERROR = 3



'''
function log black menu
'''
FUNC_BLACK_MENU = []

#######################################################################################

def post_data(url, data):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    #enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()

def get_data(url):
    return urllib2.urlopen(url).read()

def get_url(request):
    host = request.META.get("HTTP_HOST")
    path = request.META.get("PATH_INFO")
    query = request.META.get("QUERY_STRING")
    if host:
        url = "http://" + host
        if path:
            url += path
        if query:
            url += "?" + query
    else:
        url = WEB_URL
    return url

def auth_user(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        request = args[0]
        name = request.session.get("django_name")
        code = request.GET.get("code")
        if name or code:
            result = func(*args, **kwargs)
            return result
        else:
            host = request.META.get("HTTP_HOST")
            url = "http://" + host
            url += REDIRECT_URL + get_url(request)
            return redirect(AUTH_URL+url)

    return decorator


def datetime2str(dt, _format=r'%Y-%m-%d %H:%M:%S'):
    if dt:
        result = dt.strftime(_format)
    else:
        result = ""
    return result


def str2datetime(time_str, _format=r'%Y-%m-%d %H:%M:%S'):
    if time_str:
        result = datetime.datetime.strptime(time_str, _format)
    else:
        result = None
    return result

def time2datetime(number, _format=r'%Y-%m-%d %H:%M:%S'):
    number = float(number)
    result = time.strftime(_format, time.localtime(number))
    return result

def success_result_http(data=None):
    result = Result(LOWER_STATUS_SUCCESS,
                    "",
                    data)
    return result.http()

def fail_result_http(message="", data=None):
    result = Result(LOWER_STATUS_FAIL,
                    message,
                    data)
    return result.http()

def exception_result_http():
    result = Result()
    return result.exception_http()

class Result(object):
    def __init__(self,
                 status=LOWER_STATUS_SUCCESS,
                 message="",
                 data=None):
        self.result = {"status":status,
                       "message":message,
                       "data":data}

    def set_success(self):
        self.result["status"] = LOWER_STATUS_SUCCESS

    def set_fail(self):
        self.result["status"] = LOWER_STATUS_FAIL

    def set_message(self, message):
        self.result["message"] = message

    def set_data(self, data):
        self.result["data"] = data

    def json(self):
        return self.result

    def http(self, code=200):
        result = self._dumps()
        return HttpResponse(result, "application/json", code)

    def exception_http(self):
        self.set_fail()
        self.set_message(traceback.format_exc())
        self.set_data(None)
        return self.http(500)

    def exception_json(self):
        self.set_fail()
        self.set_message(traceback.format_exc())
        self.set_data(None)
        return self.json()

    def _dumps(self):
        return json.dumps(self.result)

def paging_algorithm(total, page_current):
    '''
    :param total: 记录总条数
    :param current: 当前页码
    :return:
    '''
    ret = {}
    if total > PAGING_NUM:
        ret["total"] = total
        ret["page"] = {}
        start = (page_current-1) * PAGING_NUM
        end = page_current * PAGING_NUM if page_current * PAGING_NUM < total else total
        page_total = int(math.ceil(total * 1.0 / PAGING_NUM))
        page_start = 1
        page_end = page_total + 1
        if page_total > MAX_PAGING:
            half = MAX_PAGING/2
            if page_current + half > page_end:
                page_start = page_end - 2 * half
            if page_current - half < page_start:
                page_end = page_start + 2 * half
            if page_current + half <= page_end and page_current - half >= page_start:
                page_start = page_current - half
                page_end = page_current + half + 1

        if page_current == 1:
            flag = "start"
        elif page_current == page_total:
            flag = "end"
        else:
            flag = "other"
        ret["start"] = start
        ret["end"] = end
        ret["flag"] = flag
        ret["page"]["current"] = page_current
        ret["page"]["total"] = page_total
        ret["page"]["start"] = page_start
        ret["page"]["end"] = page_end
        ret["page"]["list"] = range(page_start, page_end)
    return ret

def get_user_mail(request):
    return request.session.get("django_mail") if request.session.get("django_mail") else ""

class Model():
    '''
    对数据库操作类
    '''
    def __init__(self, model=None):
        self.model = model

    def get_list(self):
        '''
        获取所有列表数据
        '''
        ret = []
        if self.model:
            for model in self.model:
                try:
                    ret.append(model_to_dict(model))
                except:
                    pass
        return ret

    def get_dict(self):
        '''
        获取指定id的字典数据
        '''
        ret = {}
        if id and self.model:
            ret = model_to_dict(self.model)
        return ret

    def save_dict(self, data):
        '''
        保存字典数据，适合无unique字段
        '''
        if isinstance(data, dict) and self.model:
            for key, value in data.iteritems():
                if hasattr(self.model, key):
                    setattr(self.model, key, value)
            self.model.save()

    def save_unique(self, data):
        '''
        保存含有unique字段的字典数据
        '''
        if isinstance(data, dict):
            for key, value in data.iteritems():
                if hasattr(self.model, key):
                    setattr(self.model, key, value)
            self.model.save()


