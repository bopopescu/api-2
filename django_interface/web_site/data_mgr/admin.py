# coding:utf8
'''
Created on 2015-02-14

@author: liliurd
'''

from django.contrib import admin
import models


class ApiWorkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'description', 'is_show']
    search_fields = ['name', 'user']

admin.site.register(models.ApiWork, ApiWorkAdmin)


class ApiGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'description', 'is_show']
    search_fields = ['name', 'user']

admin.site.register(models.ApiGroup, ApiGroupAdmin)


class ApiAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_id', 'name', 'url', 'url_param', 'user', 'badge', 'create']
    search_fields = ['name', 'url_param', "user"]

admin.site.register(models.Api, ApiAdmin)


class ApiParamsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'api_id', 'api_type']

admin.site.register(models.ApiParams, ApiParamsAdmin)


class DataStructureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'user', 'is_base', "status"]

admin.site.register(models.DataStructure, DataStructureAdmin)


class UrlHostAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'user', 'description']

admin.site.register(models.UrlHost, UrlHostAdmin)

class ApiCollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'api_id', 'user']

admin.site.register(models.ApiCollection, ApiCollectionAdmin)

class ApiRankingAdmin(admin.ModelAdmin):
    list_display = ['id', 'work', 'path', 'total', 'create']
    search_fields = ['work', 'path']
admin.site.register(models.ApiRanking, ApiRankingAdmin)

class ApiTagsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'description']
    search_fields = ['name', 'user']
admin.site.register(models.ApiTags, ApiTagsAdmin)