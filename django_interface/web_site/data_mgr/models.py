# coding:utf8
'''
Created on 2015-02-14

@author: liliurd
'''

from django.db import models
# Create your models here.


class ApiWork(models.Model):
    name = models.CharField(unique=True, max_length=128, verbose_name=u'名称')
    user = models.CharField(db_index=True, max_length=32, null=True, blank=True, verbose_name=u'负责人')
    create = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    is_show = models.BooleanField(db_index=True, default=True, verbose_name=u'是否展现')
    description = models.TextField(blank=True, null=True, verbose_name=u'描述')
    options = models.TextField(blank=True, null=True, verbose_name=u'自定义')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"API业务"
        verbose_name_plural = u"API业务"


class ApiGroup(models.Model):
    work_id = models.IntegerField(db_index=True, default=0, verbose_name=u'所属业务')
    name = models.CharField(db_index=True, max_length=128, null=True, blank=True, verbose_name=u'名称')
    is_show = models.BooleanField(db_index=True, default=True, verbose_name=u'是否展现')
    user = models.CharField(db_index=True, max_length=32, null=True, blank=True, verbose_name=u'负责人')
    create = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    description = models.TextField(blank=True, null=True, verbose_name=u'描述')
    options = models.TextField(blank=True, null=True, verbose_name=u'自定义')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"API分组"
        verbose_name_plural = u"API分组"


class Api(models.Model):
    group_id = models.IntegerField(db_index=True, default=0, verbose_name=u'所属分组')
    name = models.CharField(db_index=True, max_length=128, blank=True, null=True, verbose_name=u'接口名称')
    url = models.CharField(db_index=True, max_length=128, blank=True, null=True, verbose_name=u'url host')
    url_param = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'url参数')
    status = models.CharField(db_index=True, max_length=32, blank=True, null=True, verbose_name=u'状态')
    request_type = models.CharField(db_index=True, max_length=32, blank=True, null=True, verbose_name=u'请求方式')
    is_show = models.BooleanField(db_index=True, default=True, verbose_name=u'是否展现')
    user = models.CharField(db_index=True, max_length=32, null=True, blank=True, verbose_name=u'负责人')
    create = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    modify = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    version = models.CharField(db_index=True, max_length=128, blank=True, verbose_name=u'版本')
    mob_version_id = models.IntegerField(db_index=True, default=0, blank=True, null=True, verbose_name=u'客户端版本')
    slave_api = models.IntegerField(db_index=True, default=0, blank=True, verbose_name=u'隶属api')
    badge = models.IntegerField(db_index=True, default=0, verbose_name=u'徽章')
    description = models.TextField(blank=True, null=True, verbose_name=u'描述')
    in_param = models.TextField(blank=True, null=True, verbose_name=u'输入参数')
    out_param = models.TextField(blank=True, null=True, verbose_name=u'输出参数')
    ret_param = models.TextField(blank=True, null=True, verbose_name=u'返回值')
    error_param = models.TextField(blank=True, null=True, verbose_name=u'错误码')
    options = models.TextField(blank=True, null=True, verbose_name=u'示例')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"API详情"
        verbose_name_plural = u"API详情"

class ApiParams(models.Model):
    api_id = models.IntegerField(db_index=True, default=0, verbose_name=u'接口id')
    api_type = models.IntegerField(db_index=True, default=0, verbose_name=u'参数类型')
    name = models.CharField(db_index=True, max_length=128, blank=True, null=True, verbose_name=u'关键值')
    params = models.TextField(blank=True, null=True, verbose_name=u'参数详情')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"API参数"
        verbose_name_plural = u"API参数"


class DataStructure(models.Model):
    name = models.CharField(unique=True, max_length=128, verbose_name=u'名称')
    description = models.TextField(blank=True, null=True, verbose_name=u'描述')
    is_base = models.BooleanField(db_index=True, default=True, verbose_name=u'是否基本')
    user = models.CharField(db_index=True, max_length=32, null=True, blank=True, verbose_name=u'负责人')
    status = models.CharField(db_index=True, max_length=32, blank=True, null=True, verbose_name=u'状态')
    detail = models.TextField(blank=True, null=True, verbose_name=u'结构详情')
    options = models.TextField(blank=True, null=True, verbose_name=u'自定义')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"数据结构表"
        verbose_name_plural = u"数据结构表"


class UrlHost(models.Model):
    host = models.CharField(unique=True, max_length=128, verbose_name=u'域名')
    user = models.CharField(db_index=True, max_length=32, null=True, blank=True, verbose_name=u'创建人')
    description = models.TextField(blank=True, null=True, verbose_name=u'描述')

    def __unicode__(self):
        return self.host

    class Meta:
        verbose_name = u"域名表"
        verbose_name_plural = u"域名表"


class ApiCollection(models.Model):
    user = models.CharField(db_index=True, max_length=32, null=True, blank=True, verbose_name=u'负责人')
    api_id = models.IntegerField(db_index=True, default=0, verbose_name=u'接口id')

    class Meta:
        unique_together = (("user", "api_id"),)
        verbose_name = u"API收藏"
        verbose_name_plural = u"API收藏"


class ApiRanking(models.Model):
    work = models.CharField(db_index=True, max_length=64, null=True, blank=True, verbose_name=u'模块名')
    path = models.CharField(db_index=True, max_length=128, null=True, blank=True, verbose_name=u'url路径')
    total = models.IntegerField(db_index=True, default=0, null=True, blank=True, verbose_name=u'访问量')
    create = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __unicode__(self):
        return "%s\t%s" % (self.work, self.path)

    class Meta:
        verbose_name = u"api排行榜"
        verbose_name_plural = u"api排行榜"

class MobVersion(models.Model):
    name = models.CharField(unique=True, max_length=128, verbose_name=u'版本名')
    user = models.CharField(db_index=True, max_length=32, null=True, blank=True, verbose_name=u'创建人')
    description = models.TextField(blank=True, null=True, verbose_name=u'描述')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"客户端版本"
        verbose_name_plural = u"客户端版本"

class ApiTags(models.Model):
    name = models.CharField(unique=True, max_length=128, verbose_name=u'标签名')
    user = models.CharField(db_index=True, max_length=32, null=True, blank=True, verbose_name=u'创建人')
    description = models.TextField(blank=True, null=True, verbose_name=u'描述')

    class Meta:
        verbose_name = u"API标签"
        verbose_name_plural = u"API标签"

class ApiTagsSet(models.Model):
    api_id = models.IntegerField(db_index=True, default=0, verbose_name=u'接口id')
    tag_id = models.IntegerField(db_index=True, default=0, verbose_name=u'标签id')

    class Meta:
        verbose_name = u"API标签集合"
        verbose_name_plural = u"API标签集合"
