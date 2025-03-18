import django
from django.contrib import admin
from django.urls import path, include, re_path
# 导入xadmin，替换admin
from django.views.static import serve

import users
import xadmin
from django.views.generic import TemplateView
# from users.views import user_login
from CourseOnline.settings import MEDIA_ROOT
from organization.views import OrgView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, LogoutView, \
    IndexView

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # TemplateView.as_view会将template转换为view
    # path('', TemplateView.as_view(template_name= "index.html"), name=  "index"),
    path('', IndexView.as_view(), name="index"),
    # 基于类方法实现登录,这里是调用它的方法
    path('login/', LoginView.as_view(), name="login"),
    # 退出功能url
    path('logout/', LogoutView.as_view(), name="logout"),

    # 注册url
    path("register/", RegisterView.as_view(), name="register"),

    # 验证码url
    path("captcha/", include('captcha.urls')),

    # 激活用户url
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name="user_active"),

    # 忘记密码
    path('forget/', ForgetPwdView.as_view(), name="forget_pwd"),

    # 重置密码urlc ：用来接收来自邮箱的重置链接
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name="reset_pwd"),

    # 修改密码url; 用于passwordreset页面提交表单
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构app的url配置，讲师的也在里面
    path("org/", include('organization.urls', namespace='org')),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    # re_path('static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),
    # 课程app的url配置
    path("course/", include('courses.urls', namespace="course")),
    # user app的url配置
    path("users/", include('users.urls', namespace="users")),

    # 富文本相关url
    path('ueditor/', include('DjangoUeditor.urls')),
]
