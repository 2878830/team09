import django
from django.contrib import admin
from django.urls import path, include, re_path
# xadmin
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
    # TemplateView.as_view template tranfer to view
    # path('', TemplateView.as_view(template_name= "index.html"), name=  "index"),
    path('', IndexView.as_view(), name="index"),
  
    path('login/', LoginView.as_view(), name="login"),
   
    path('logout/', LogoutView.as_view(), name="logout"),

    path("register/", RegisterView.as_view(), name="register"),

   
    path("captcha/", include('captcha.urls')),

  
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name="user_active"),

   
    path('forget/', ForgetPwdView.as_view(), name="forget_pwd"),

    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name="reset_pwd"),

 
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),

  
    path("org/", include('organization.urls', namespace='org')),
  
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
   
    # re_path('static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),
    
    path("course/", include('courses.urls', namespace="course")),
 
    path("users/", include('users.urls', namespace="users")),

   
    path('ueditor/', include('DjangoUeditor.urls')),
]
