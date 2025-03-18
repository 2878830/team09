# encoding: utf-8
from django.urls import path, re_path
from organization.views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, \
    AddFavView, TeacherListView, TeacherDetailView

app_name = "organization"
# 机构模块子路由 organization url
urlpatterns = [
    # 课程机构列表url list url
    path('list/', OrgView.as_view(), name="org_list"),
    # 添加我要学习 add study url
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"),
    # home页面,取纯数字 home page 
    re_path('home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name="org_home"),
    # 访问课程 interview page
    re_path('course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name="org_course"),
    # 访问机构描述 description page
    re_path('desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name="org_desc"),
    # 访问机构讲师 teachers page
    re_path('org_teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name="org_teacher"),
    # 机构收藏 organization favorite
    path('add_fav/', AddFavView.as_view(), name="add_fav"),
    # 讲师列表 teacher list
    path('teacher/list/', TeacherListView.as_view(), name="teacher_list"),
    # 访问机构讲师 detail page
    re_path('teacher/detail/(?P<teacher_id>\d+)/', TeacherDetailView.as_view(), name="teacher_detail"),
]
