import json

from courses.models import Course
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
# 进行密码加密 password 
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from pure_pagination import Paginator, PageNotAnInteger
# 发送邮件 send email
from utils.email_send import send_register_eamil

# form表单验证 & 验证码 about form
from .forms import LoginForm, RegisterForm, ActiveForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from .models import UserProfile, EmailVerifyRecord, Banner


# 激活用户的view active user
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在 whether is it exist
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 如果不为空也就是有用户 users exists
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱 email 
                email = record.email
                # 查找到邮箱对应的user find user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功跳转到登录页面 login page 
                return render(request, "login.html", )
        else:
            return render(
                request, "register.html", {
                    "msg": "Your activation link is invalid", "active_form": active_form})


# 注册功能的view register
class RegisterView(View):
    # get方法直接返回页面 return html
    def get(self, request):
        # 添加验证码 add captcha
        register_form = RegisterForm()
        return render(
            request, "register.html", {
                'register_form': register_form})

    def post(self, request):
        # 实例化form instance register_form
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 这里注册时前端的name为email register form
            user_name = request.POST.get("email", "")
            # 用户查重 users exists
            if UserProfile.objects.filter(email=user_name):
                return render(
                    request, "register.html", {
                        "register_form": register_form, "msg": "User already exists"})
            pass_word = request.POST.get("password", "")

            # 实例化一个user_profile对象，将前台值存入 instance user_profile
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name

            # 默认激活状态为false default is false
            user_profile.is_active = False

            # 加密password进行保存 save password
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入欢迎注册消息 write message
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "Welcome to LearnEase!! -- System automatic message"
            user_message.save()
            # 发送注册激活邮件 send email
            send_register_eamil(user_name, "register")

            # 跳转到登录页面 jump to login page
            return render(request, "login.html", )
        # 注册邮箱form验证失败 failure
        else:
            return render(
                request, "register.html", {
                    "register_form": register_form})


# 验证用户 users login
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询 not suppose to have two users with the same email or username
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username))
            # django的后台中密码加密：所以不能password==password 
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 退出登录 login out
class LogoutView(View):
    def get(self, request):
        # django自带的logout 
        logout(request)
        # 重定向到首页, redirect to index
        return HttpResponseRedirect(reverse("index"))


# 登录 login
class LoginView(View):
    # 直接调用get方法免去判断 get method 
    def get(self, request):
        # render就是渲染html返回用户 return html
        # render三变量: request 模板名称 一个字典写明传给前端的值 return variables
        redirect_url = request.GET.get('next', '')
        return render(request, "login.html", {
            "redirect_url": redirect_url
        })

    def post(self, request):
        # 类实例化需要一个字典参数dict:request.POST就是一个QueryDict所以直接传入 instance login_form
        # POST中的usernamepassword，会对应到form中 
        login_form = LoginForm(request.POST)

        # is_valid判断我们字段是否有错执行我们原有逻辑，验证失败跳回login页面 whether is valid, return failure
        if login_form.is_valid():
            # 取不到时为空，username，password为前端页面name值 
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            # 成功返回user对象,失败返回null return user object,login failed return null
            user = authenticate(username=user_name, password=pass_word)

            # 如果不是null说明验证成功 if user not is None
            if user is not None:
                # 只有当用户激活时才给登录 only allow login when user is active
                if user.is_active:
                    # login_in 两参数：request, user 
                    # 实际是对request写了一部分东西进去，然后在render的时候： 
                    # request是要render回去的。这些信息也就随着返回浏览器。完成登录 
                    login(request, user)
                    # 跳转到首页 user request会被带回到首页 jump to index
                    # 增加重定向回原网页。
                    redirect_url = request.POST.get('next', '')
                    if redirect_url:
                        return HttpResponseRedirect(redirect_url)
                    # 跳转到首页 user request会被带回到首页 jump to index
                    return HttpResponseRedirect(reverse("index"))
                # 即用户未激活跳转登录，提示未激活 
                else:
                    return render(
                        request, "login.html", {
                            "msg": "User name is not active! Please go to your email to activate"})
            # 仅当用户真的密码出错时 error
            else:
                return render(request, "login.html", {"msg": "Wrong username or password!"})
        # 验证不成功跳回登录页面 jump to login page
        # 没有成功说明里面的值是None，并再次跳转回主页面 return login page
        else:
            return render(
                request, "login.html", {
                    "login_form": login_form})


# 当我们配置url被这个view处理时，自动传入request对象. when we use this view,
# it will automatically receive a request object.
# 这个是已经被我抛弃的方法型实现，改为类实现 this is old method
def user_login(request):
    # 前端向后端发送的请求方式: get 或post get /post

    # 登录提交表单为post submit method
    if request.method == "POST":
        # 取不到时为空，username，password为前端页面name值 not null return failure
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")

        # 成功返回user对象,失败返回null sucess return user object,login failed return null
        user = authenticate(username=user_name, password=pass_word)

        # 如果不是null说明验证成功 if user not is None
        if user is not None:
            # login_in 两参数：request, user 
            # 实际是对request写了一部分东西进去，然后在render的时候： 
            # request是要render回去的。这些信息也就随着返回浏览器。完成登录
            login(request, user)
            return render(request, "index.html")
        # 没有成功说明里面的值是None，并再次跳转回主页面 if not success return login page
        else:
            return render(request, "login.html", {"msg": "用户名或密码错误! "})

    # 获取登录页面为get login  return login page
    elif request.method == "GET":
        # render就是渲染html返回用户 return html
        # render三变量: request 模板名称 一个字典写明传给前端的值 return variables
        return render(request, "login.html", {})


# 用户忘记密码 forgot password
class ForgetPwdView(View):
    # get方法直接返回页面 return page
    def get(self, request):
        # 给忘记密码页面加上验证码 return page
        active_form = ActiveForm(request.POST)
        return render(request, "forgetpwd.html", {"active_form": active_form})

    # post方法实现 post method 
    def post(self, request):
        forget_form = ForgetForm(request.POST)
        # form验证合法情况下取出email correct return email
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            # 发送找回密码邮件 send email
            send_register_eamil(email, "forget")
            # 发送完毕返回登录页面并显示发送邮件成功。 send email success return login page
            return render(request, "login.html", {"msg": "重置密码邮件已发送,请注意查收"})
        # 如果表单验证失败也就是他验证码输错等。 if not correct return page
        else:
            return render(
                request, "forgetpwd.html", {
                    "forget_from": forget_form})


# 重置密码 reset pwd
class ResetView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在 whether email exist
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 如果不为空也就是有用户 users exist
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱 get email
                email = record.email
                # 将email传回来 transfer to email
                return render(request, "password_reset.html", {"email": email})

        else:
            return render(
                request, "forgetpwd.html", {
                    "msg": "Your password reset link is invalid, please request again", "active_form": active_form})


# 修改密码 modify pwd
class ModifyPwdView(View):
    def post(self, request):
        modiypwd_form = ModifyPwdForm(request.POST)
        if modiypwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            # 如果两次密码不相等，返回错误信息 not equal return error
            if pwd1 != pwd2:
                return render(
                    request, "password_reset.html", {
                        "email": email, "msg": "Inconsistent password"})
            # 如果密码一致 the same return success
            user = UserProfile.objects.get(email=email)
            # 加密成密文 password
            user.password = make_password(pwd2)
            # save保存到数据库
            user.save()
            return render(request, "login.html", {"msg": "Password changed successfully, please log in"})
        # 验证失败说明密码位数不够。 failure return page
        else:
            email = request.POST.get("email", "")
            return render(
                request, "password_reset.html", {
                    "email": email, "modiypwd_form": modiypwd_form})


# 用户信息 information message
class UserInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, "usercenter-info.html", {
        })

    def post(self, request):
        # 不像用户咨询是一个新的。需要指明instance。不然无法修改，而是新增用户
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(
                '{"status":"success"}',
                content_type='application/json')
        else:
            # 通过json的dumps方法把字典转换为json字符串
            return HttpResponse(
                json.dumps(
                    user_info_form.errors),
                content_type='application/json')


# 用户上传图片，用于修改头像
class UploadImageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        # 这时候用户上传的文件就已经被保存到imageform了 ，为modelform添加instance值直接保存
        image_form = UploadImageForm(
            request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            # # 取出cleaned data中的值,一个dict
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            return HttpResponse(
                '{"status":"success"}',
                content_type='application/json')
        else:
            return HttpResponse(
                '{"status":"fail"}',
                content_type='application/json')


# 在个人中心修改用户密码 center modify pwd
class UpdatePwdView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            # 如果两次密码不相等，返回错误信息
            if pwd1 != pwd2:
                return HttpResponse(
                    '{"status":"fail", "msg":"Inconsistent password"}',
                    content_type='application/json')
            # 如果密码一致 same
            user = request.user
            # 加密成密文
            user.password = make_password(pwd2)
            # save保存到数据库 save
            user.save()
            return HttpResponse(
                '{"status":"success"}',
                content_type='application/json')
    
        else:
            # 通过json的dumps方法把字典转换为json字符串 str
            return HttpResponse(
                json.dumps(
                    modify_form.errors),
                content_type='application/json')


# 发送邮箱验证码 send email code
class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        # 取出需要发送的邮件 send email
        email = request.GET.get("email", "")

        # 不能是已注册的邮箱 register   
        if UserProfile.objects.filter(email=email):
            return HttpResponse(
                '{"email":"Email already exists"}',
                content_type='application/json')
        send_register_eamil(email, "update_email")
        return HttpResponse(
            '{"status":"success"}',
            content_type='application/json')


# 修改邮箱 correct email
class UpdateEmailView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")

        existed_records = EmailVerifyRecord.objects.filter(
            email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse(
                '{"status":"success"}',
                content_type='application/json')
        else:
            return HttpResponse(
                '{"email":"Verification code is invalid"}',
                content_type='application/json')


# 个人中心页我的课程 my courses
class MyCourseView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {
            "user_courses": user_courses,
        })


# 我收藏的机构 favorite organization
class MyFavOrgView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象 only id
        for fav_org in fav_orgs:
            # 取出fav_id也就是机构的id。 the same id
            org_id = fav_org.fav_id
            # 获取这个机构对象 get the same id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
        })


# 我收藏的授课讲师 favorite teachers
class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象 only id
        for fav_teacher in fav_teachers: 
            # 取出fav_id也就是机构的id。 the same id
            teacher_id = fav_teacher.fav_id
            # 获取这个机构对象 get the same id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,
        })


# 我收藏的课程 favorite course
class MyFavCourseView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象 only id
        for fav_course in fav_courses:
            # 取出fav_id也就是机构的id。 the same id
            course_id = fav_course.fav_id
            # 获取这个机构对象 get the same id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, "usercenter-fav-course.html", {
            "course_list": course_list,
        })


# 我的消息 my message
class MyMessageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人中心消息页面，清空未读消息记录 unread messages
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        # 对课程机构进行分页 page
        # 尝试获取前台get请求传递过来的page参数 try to get the page
        # 如果是不合法的配置参数默认返回第一页 if page is not int or less than 1
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个 five per page
        p = Paginator(all_message, 4)
        messages = p.page(page)
        return render(request, "usercenter-message.html", {
            "messages": messages,
        })


# 首页view index
class IndexView(View):
    def get(self, request):
        # 取出轮播图 banner
        all_banner = Banner.objects.all().order_by('index')[:5]
        # 正常位课程 normal courses
        courses = Course.objects.filter(is_banner=False)[:6]
        # 轮播图课程取三个 get three courses
        banner_courses = Course.objects.filter()[:3]
        print(banner_courses)
        # 课程机构 organizations 
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            "all_banner": all_banner,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
        })
