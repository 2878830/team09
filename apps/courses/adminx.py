# encoding: utf-8

import xadmin

from .models import Course, Lesson, Video, CourseResource


# Course的admin管理器 Course administrator
class CourseAdmin(object):
    list_display = [
        'name',
        'desc',
        'detail',
        'degree',
        'learn_times',
        'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = [
        'name',
        'desc',
        'detail',
        'degree',
        'learn_times',
        'students']
    # 富文本 Rich text
    style_fields = {"detail": "ueditor"}


# 章节管理  Chapter management
class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    # __name represents using the name field in foreign key  # __name代表使用外键中name字段
    list_filter = ['course__name', 'name', 'add_time']


# 视频管理 Video management
class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


# 课程资源管理 Course resource management
class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


# 将管理器与model进行注册关联 Register the model and the manager
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
