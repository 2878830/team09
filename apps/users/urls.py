# encoding: utf-8

from django.urls import path
from users.views import UserInfoView, UploadImageView, SendEmailCodeView, UpdateEmailView, UpdatePwdView, MyCourseView, \
    MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

app_name = "users"

# 用户模块子路由 users url
urlpatterns = [
    # 用户信息 information message
    path('info/', UserInfoView.as_view(), name="user_info"),
    # 用户头像上传 upload image
    path('image/upload/', UploadImageView.as_view(), name="image_upload"),
    # 用户个人中心修改密码 change password
    path('update/pwd/', UpdatePwdView.as_view(), name="update_pwd"),
    # 专用于发送验证码的 send email code
    path('sendemail_code/',SendEmailCodeView.as_view(),name="sendemail_code"),
    # 修改邮箱 correct email
    path('update_email/', UpdateEmailView.as_view(), name="update_email"),
    # 用户中心我的课程 my cources
    path('mycourse/', MyCourseView.as_view(), name="mycourse"),
    # 我收藏的课程机构 organization favorite
    path('myfav/org/', MyFavOrgView.as_view(), name="myfav_org"),
    # 我收藏的授课讲师 teachers favorite
    path('myfav/teacher/', MyFavTeacherView.as_view(), name="myfav_teacher"),
    # 我收藏的课程 favorite course
    path('myfav/course/', MyFavCourseView.as_view(), name="myfav_course"),
    # 我的消息 message
    path('my_message/', MyMessageView.as_view(), name="my_message"),
]
