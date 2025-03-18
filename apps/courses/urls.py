# encoding: utf-8
from courses.views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView, VideoPlayView
from django.urls import path, re_path

app_name = "courses"
# 课程管理子路由 urlpatterns
urlpatterns = [
    # 课程列表url 
    # #Course List URL
    path('list/', CourseListView.as_view(), name="list"),
    # 课程详情页
    #Course Detail Page
    re_path('detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),
    # 课程章节信息页
    #Course Chapter Info Page
    re_path('info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),
    # 课程章节信息页
    #Course Chapter Info Page
    re_path('comments/(?P<course_id>\d+)/', CommentsView.as_view(), name="course_comments"),
    # 添加课程评论
    #Add Course Comment
    path('add_comment/', AddCommentsView.as_view(), name="add_comment"),
    # 课程视频播放页 
    # # Course Video Playback Page
    re_path('video/(?P<video_id>\d+)/', VideoPlayView.as_view(), name="video_play"),
]
