from courses.models import Course, CourseResource, Video
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from operation.models import UserFavorite, CourseComments, UserCourse
from pure_pagination import Paginator, PageNotAnInteger


# 课程列表 
# Course List
class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all()
        # 热门课程推荐
        # Recommended Popular Courses
        hot_courses = Course.objects.all().order_by("-students")[:3]
        # 搜索功能
        # Search Function
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # Conduct operations on the "name" field, performing operations of the "like" statement. Here, "i" indicates case-insensitivity. 
            # or操作使用Q
            # Using Q for OR operations
            all_course = all_course.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                detail__icontains=search_keywords))
        # 对课程进行分页
        # Paginate the courses
        # 尝试获取前台get请求传递过来的page参数
        # Try to obtain the "page" parameter passed in through the front-end GET request. 
        # 如果是不合法的配置参数默认返回第一页
        # If the configuration parameters are invalid, return the first page by default.
        # 进行排序
        # Perform sorting.
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_course = all_course.order_by("-students")
            elif sort == "hot":
                all_course = all_course.order_by("-click_nums")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个
        # Here it means to take five items from "allorg", and display five items per page.
        p = Paginator(all_course, 6, request=request)
        courses = p.page(page)
        return render(request, "course-list.html", {
            "all_course": courses,
            "sort": sort,
            "hot_courses": hot_courses,
            "search_keywords": search_keywords
        })


# 课程详情
# Course Details
class CourseDetailView(View):
    def get(self, request, course_id):
        # 此处的id为表默认为我们添加的值。
        # Here, the "id" is the value that the table adds for us by default.
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        # Increase the click count of the course.
        course.click_nums += 1
        course.save()

        # 是否收藏课程
        # Whether to collect the course
        has_fav_course = False
        has_fav_org = False

        # 必须是用户已登录我们才需要判断。
        # We only need to make the judgment when the user is logged in.
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        # 取出标签找到标签相同的course
        # Retrieve the tags and find the courses with the same tags.
        tag = course.tag
        if tag:
            # 从1开始否则会推荐自己
            # Start from 1, otherwise it will recommend itself. 
            relate_courses = Course.objects.filter(tag=tag)[1:2]
        else:
            relate_courses = []
        return render(request, "course-detail.html", {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


# 课程章节信息
# Course Chapter Info
class CourseInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, course_id):
        # 此处的id为表默认为我们添加的值。
        # The ID here is the value that the table adds for us by default. 
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否开始学习了该课，如果还未学习则，加入用户课程表
        # Query whether the user has started learning this course. If the user hasn't started learning it yet, add it to the user's course list. 
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            course.students += 1
            course.save()
            user_course.save()
        # 查询课程资源
        # Query course resources.
        all_resources = CourseResource.objects.filter(course=course)
        # 选出学了这门课的学生关系 
        # Select the student relationships of those who have taken this course. 
        user_courses = UserCourse.objects.filter(course=course)
        # 从关系中取出user_id
        # Extract the "user_id" from the relationship.
        user_ids = [user_course.user_id for user_course in user_courses]
        # 这些用户学了的课程,外键会自动有id，取到字段
        # For the courses that these users have studied, the foreign key will automatically have an ID. Retrieve the fields. 
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        # Retrieve all the course IDs.
        course_ids = [user_course.course_id for user_course in all_user_courses]
        # 获取学过该课程用户学过的其他课程 Get other courses taken by users who have taken this course
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums").exclude(id=course.id)[:4]
        # 是否收藏课程 Whether the course has been favorited. 
        return render(request, "course-video.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
        })


# 课程评论 comment
class CommentsView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, course_id):
        # 此处的id为表默认为我们添加的值。 default
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course).order_by("-add_time")
        # 选出学了这门课的学生关系 relationship
        user_courses = UserCourse.objects.filter(course=course)
        # 从关系中取出user_id
        #Extract user_id from relation
        user_ids = [user_course.user_id for user_course in user_courses]
        # 这些用户学了的课程,外键会自动有id，取到字段
        #These users' learned courses, foreign key auto-generates ID, extract field
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        # Retrieve all the course IDs.
        course_ids = [user_course.course_id for user_course in all_user_courses]
        # 获取学过该课程用户学过的其他课程
        #Get other courses learned by users who studied this course
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums").exclude(id=course.id)[:4]
        # 是否收藏课程 bookmark
        return render(request, "course-comment.html", {
            "course": course,
            "all_resources": all_resources,
            "all_comments": all_comments,
            "relate_courses": relate_courses,
        })


# ajax请求添加评论
#Ajax request to add comment
class AddCommentsView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"User not logged in"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            # get只能取出一条数据，如果有多条抛出异常。没有数据也抛异常
            # filter取一个列表出来，queryset。没有数据返回空的queryset不会抛异常
            course = Course.objects.get(id=int(course_id))
            # 外键存入要存入对象
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"Review success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"Comment failure"}', content_type='application/json')


# 视频播放
class VideoPlayView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, video_id):
        # 此处的id为表默认为我们添加的值。
        video = Video.objects.get(id=int(video_id))
        # 找到对应的course
        course = video.lesson.course
        # 查询用户是否开始学习了该课，如果还未学习则，加入用户课程表
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 查询课程资源
        all_resources = CourseResource.objects.filter(course=course)
        # 选出学了这门课的学生关系
        user_courses = UserCourse.objects.filter(course=course)
        # 从关系中取出user_id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 这些用户学了的课程,外键会自动有id，取到字段
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course_id for user_course in all_user_courses]
        # 获取学过该课程用户学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums").exclude(id=course.id)[:4]
        # 是否收藏课程
        return render(request, "course-play.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
            "video": video,
        })
