# encoding: utf-8
from courses.models import Course
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from operation.models import UserFavorite
from organization.forms import UserAskForm
from pure_pagination import Paginator, PageNotAnInteger

from .models import CourseOrg, CityDict, Teacher


# 机构信息 information 
class OrgView(View):
    def get(self, request):
        # 查找到所有的课程机构 find all course org
        all_orgs = CourseOrg.objects.all()
        # 查询最新机构的课程数量和总的学习人数 find all course org and numbers of students
        for org in all_orgs:
            students = 0
            org.course_nums = len(Course.objects.filter(course_org=org.id))
            for c in Course.objects.filter(course_org=org.id):
                students += c.students
            org.students = students
            org.save()
        # 热门机构,如果不加负号会是有小到大。 hot org ,if you want to sort by students,you can use -students
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 搜索功能 seek keyword
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写 operation on name field 
            # or操作使用Q or Q or
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                address__icontains=search_keywords))
        # 取出所有的城市 all city
        all_city = CityDict.objects.all()

        # 取出筛选的城市,默认值为空 city_id
        city_id = request.GET.get('city', "")
        # 如果选择了某个城市,也就是前端传过来了值 if choose city,we will filter the courseorg by city
        if city_id:
            # 外键city在数据中叫city_id foreign key city id
            # 我们就在机构中作进一步筛选 choose city
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选 category 
        category = request.GET.get('ct', "")
        if category:
            # 我们就在机构中作进一步筛选类别 choose category
            all_orgs = all_orgs.filter(category=category)

        # 进行排序 rank 
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 总共有多少家机构使用count进行统计 count the number of orgs
        org_nums = all_orgs.count()
        # 对课程机构进行分页 page
        # 尝试获取前台get请求传递过来的page参数 try to
        # 如果是不合法的配置参数默认返回第一页 IF the page parameter is not a number, return the first page
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个 IF the page parameter is not a number, return the first page
        p = Paginator(all_orgs, 4, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_city": all_city,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
            "search_keywords": search_keywords,
        })


# 用户添加咨询 ask
class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"Your field has errors, please check"}', content_type='application/json')


# 机构首页 page
class OrgHomeView(View):
    def get(self, request, org_id):
        # 向前端传值，表明现在在home页 current_page
        current_page = "home"
        # 根据id取到课程机构 according to id find the course org according to id
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        # 向前端传值说明用户是否收藏 wheather the user has fav the org
        has_fav = False
        # 必须是用户已登录我们才需要判断。 login user only
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用 foreignkey reference
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]

        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teacher': all_teacher,
            'course_org': course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })


# 机构课程列表页 list page
class OrgCourseView(View):
    def get(self, request, org_id):
        # 向前端传值，表明现在在home页 current_page
        current_page = "course"
        # 根据id取到课程机构 according to id
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用 find the course according to courseorg
        all_courses = course_org.course_set.all()
        print(all_courses)
        # 向前端传值说明用户是否收藏 wheather the user has fav the org
        has_fav = False
        # 必须是用户已登录我们才需要判断。 login user only
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


# 机构描述详情页 details page
class OrgDescView(View):
    def get(self, request, org_id):
        # 向前端传值，表明现在在home页 current_page
        current_page = "desc"
        # 根据id取到课程机构 according to id
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用 find the course according to courseorg
        # 向前端传值说明用户是否收藏 wheather the user has fav the org
        has_fav = False
        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


# 机构讲师列表页 teacher list
class OrgTeacherView(View):
    def get(self, request, org_id):
        # 向前端传值，表明现在在home页 current_page
        current_page = "teacher"
        # 根据id取到课程机构 according to id
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用 find the course according to courseorg
        all_teachers = course_org.teacher_set.all()
        # 向前端传值说明用户是否收藏 wheather the user has fav the org
        has_fav = False
        # 必须是用户已登录我们才需要判断。 login user only
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })


# 用户收藏与取消收藏功能 add fav
class AddFavView(View):
    def post(self, request):
        # 表明你收藏的不管是课程，讲师，还是机构。他们的id whether you are collecting course, teacher, or org
        # 默认值取0是因为空串转int报错 default value is 0
        id = request.POST.get('fav_id', 0)
        # 取到你收藏的类别，从前台提交的ajax请求中取 category type
        type = request.POST.get('fav_type', 0)

        # 收藏与已收藏取消收藏 add fav or cancel fav
        # 判断用户是否登录:即使没登录会有一个匿名的user if user not login
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的 return HttpResponse('{"status":"fail", "msg":"User not logged in"}', content_type='application/json')
            return HttpResponse('{"status":"fail", "msg":"User not logged in"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))
        if exist_records:
            # 如果记录已经存在， 则表示用户取消收藏 if exist record
            exist_records.delete()
            if int(type) == 1:
                course = Course.objects.get(id=int(id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(type) == 2:
                org = CourseOrg.objects.get(id=int(id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            elif int(type) == 3:
                teacher = Teacher.objects.get(id=int(id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            # 过滤掉未取到fav_id type的默认情况 if type or id is not exist
            if int(type) > 0 and int(id) > 0:
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.user = request.user
                user_fav.save()

                if int(type) == 1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums += 1
                    course.save()
                elif int(type) == 2:
                    org = CourseOrg.objects.get(id=int(id))
                    org.fav_nums += 1
                    org.save()
                elif int(type) == 3:
                    teacher = Teacher.objects.get(id=int(id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"Have already collected"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"Collection error"}', content_type='application/json')


# 课程讲师列表页 teacher list
class TeacherListView(View):
    def get(self, request):
        all_teacher = Teacher.objects.all()
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_teacher = all_teacher.order_by("-click_nums")

        # 搜索功能 search
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写 
            #Perform LIKE operation on name field (i for case-insensitive)
            # or操作使用Q  
            all_teacher = all_teacher.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords))

        # 排行榜讲师 rank teacher
        rank_teacher = Teacher.objects.all().order_by("-fav_nums")[:5]
        # 总共有多少老师使用count进行统计 teacher nums
        teacher_nums = all_teacher.count()
        # 对讲师进行分页 teacher page
        # 尝试获取前台get请求传递过来的page参数 try to get the page parameter
        # 如果是不合法的配置参数默认返回第一页 if page is not a number, return the first page
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个 per page 
        p = Paginator(all_teacher, 4, request=request)
        teachers = p.page(page)
        return render(request, "teachers-list.html", {
            "all_teacher": teachers,
            "teacher_nums": teacher_nums,
            "sort": sort,
            "rank_teachers": rank_teacher,
            "search_keywords": search_keywords,
        })


# 教师详情页面 details teacher details
class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_course = teacher.course_set.all()
        # 排行榜讲师 rank teacher
        rank_teacher = Teacher.objects.all().order_by("-fav_nums")[:5]

        has_fav_teacher = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_fav_teacher = True
        has_fav_org = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_fav_org = True
        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "all_course": all_course,
            "rank_teacher": rank_teacher,
            "has_fav_teacher": has_fav_teacher,
            "has_fav_org": has_fav_org,
        })
