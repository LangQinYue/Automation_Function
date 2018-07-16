# coding:utf8
__author__ = 'lang.qy'
from django.conf.urls import url
from . import views

# login page
urlpatterns = [url(r"^$", views.login_page, name="signin"), ]
urlpatterns += [url(r"^logout/$", views._logout, name="logout"), ]

# index page
urlpatterns += [url(r"^index/$", views.index, name="index"), ]

# element list
urlpatterns += [url(r"^element/$", views.element, name="element"), ]

# test
urlpatterns += [url(r"^test/$", views.test, name="test")]

# case
urlpatterns += [url(r'^add_case/$', views.add_case, name="case")]
# edit_case
urlpatterns += [url(r'^edit_case/$', views.edit_case, name="edit_case")]

# case list
urlpatterns += [url(r"^case_list/$", views.case_list, name="case_list")]

# case_scenario list
urlpatterns += [url(r"^scenario_list/$", views.scenario_list, name="case_scenario")]

# add case scenario
urlpatterns += [url(r"^add_scenario/$", views.add_case_scenario, name="add_case_scenario")]

# edit scenario
urlpatterns += [url(r"^edit_scenario/$", views.edit_scenario, name="edit_scenario")]

# ajax html
urlpatterns += [url(r"^ajax_html/$", views.ajax_html, name="ajax_html")]

# report html

urlpatterns += [url(r'report/(.*)$', views.report, name="report")]

urlpatterns += [url(r'project/$', views.project, name="project")]
# is html path

urlpatterns += [url(r"^is_html_path/$", views.is_html_path, name="is_html_path")]

# urlpatterns += [url(r"^report/image/image/(.*)$", views.report_imgae, name="report_imgae")]
