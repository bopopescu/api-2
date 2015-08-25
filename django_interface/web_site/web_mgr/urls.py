# coding:utf8
'''
Created on 2015-02-14

@author: liliurd
'''


import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^redirect_login', views.redirect_login),
    url(r'^$', views.home),
    url(r'^get/interface', views.get_interface_view),
    url(r'^add/interface', views.add_interface_view),
    url(r'^show/interface$', views.interface_show_view),
    url(r'^show/interface/api', views.interface_show_api_view),
    url(r'^data/structure', views.get_data_structure_view),
    url(r'^save/structure', views.save_data_structure_view),
    url(r'^get/group', views.get_group_view),
    url(r'^add/group', views.add_group_view),
    url(r'^add/work', views.add_work_view),
    url(r'^get/user', views.get_user_info_view),
    url(r'^get/write', views.get_write_user_info_view),
    url(r'^set/auth', views.set_auth_view),
    url(r'^get/host', views.get_url_host_list_view),
    url(r'^edit/host', views.edit_url_host_view),
    url(r'^left/menu', views.left_menu_view),
    url(r'^main', views.main_view),
    url(r'^help', views.help_view),
    url(r'^self/bench', views.self_bench_view),
    url(r'^user/logout', views.user_logout_view),
    url(r'^api/ranking', views.api_ranking_view),
    url(r'^query/api', views.query_api_view),
)
