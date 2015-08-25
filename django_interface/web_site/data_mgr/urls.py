# coding:utf8
'''
Created on 2015-02-14

@author: liliurd
'''


import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^get/api/work', views.get_api_work_view),
    url(r'^get/api/group', views.get_api_group_view),
    url(r'^get/api/list', views.get_api_list_view),
    url(r'^get/api_all_version', views.get_api_all_version_view),
    url(r'^check/work', views.check_work_name_view),
    url(r'^check/structure', views.check_structure_name_view),
    url(r'^update/structure', views.update_structure_view),
    url(r'^delete/structure', views.delete_structure_view),
    url(r'^update/api', views.update_api_view),
    url(r'^delete/api', views.delete_api_view),
    url(r'^delete/group', views.delete_group_view),
    url(r'^delete/work', views.delete_work_view),
    url(r'^get/all', views.get_menu_tree_data_view),
    url(r'^check/host', views.check_host_view),
    url(r'^filter/api', views.filter_api_view),
    url(r'^auto/save/api', views.auto_save_api_view),
    url(r'^copy/api', views.copy_api_view),
    url(r'^delete/host', views.delete_host_view),
    url(r'^save/collection', views.save_collection_view),
    url(r'^self/bench', views.self_bench_view),
    url(r'^filter/group', views.filter_group_view),
    url(r'^add/url/api', views.add_url_api_view),
    url(r'^get/host', views.get_url_host_view),
    url(r'^set/api/badge', views.set_api_badge_view),
    url(r'^get/api/ranking', views.get_api_ranking_view),
    url(r'^user/top/ranking', views.user_top_ranking_view),
    url(r'^save/mob_version', views.save_mob_version_view),
    url(r'^get/mob_version_list', views.get_mob_version_list_view),
    url(r'^get/mob_version_dict', views.get_mob_version_dict_view),
    url(r'^update/mob_version', views.update_api_mob_version_view),

    url(r'^save/api_tag', views.save_api_tag_view),
    url(r'^bind/api_tag', views.bind_api_tag_view),
    url(r'^get/api_tag_list', views.get_api_tag_list_view),
    url(r'^get/api_tag_dict', views.get_api_tag_dict_view),
    url(r'^get/tag_set_list', views.get_tag_set_list_view),
)
