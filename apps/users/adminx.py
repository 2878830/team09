# encoding: utf-8
import xadmin
from courses.models import Course, Video, Lesson, CourseResource
from django.contrib.auth.models import Group, Permission
from operation.models import CourseComments, UserFavorite, UserMessage, UserCourse, UserAsk
from organization.models import CityDict, Teacher, CourseOrg
# 和X admin的view绑定
from xadmin import views
from xadmin.models import Log

from .models import EmailVerifyRecord, Banner, UserProfile


# X admin的全局配置信息设置
class BaseSetting(object):
    # 主题功能开启
    enable_themes = True
    use_bootswatch = True


# xadmin 全局配置参数信息设置
class GlobalSettings(object):
    site_title = "Online Course Learning System"
    site_footer = "Copyright(C). Create By BHML 2024, All Rights Reserved"

    # 收起菜单
    # menu_style = "accordion"

    def get_site_menu(self):
        return (
            {'title': 'Organization Management', 'menus': (
                {'title': 'City', 'url': self.get_model_url(CityDict, 'changelist')},
                {'title': 'Organization Info', 'url': self.get_model_url(CourseOrg, 'changelist')},
                {'title': 'Teachers', 'url': self.get_model_url(Teacher, 'changelist')},
            )},
            {'title': 'Course Management', 'menus': (
                {'title': 'Course Info', 'url': self.get_model_url(Course, 'changelist')},
                {'title': 'Lesson Info', 'url': self.get_model_url(Lesson, 'changelist')},
                {'title': 'Video Info', 'url': self.get_model_url(Video, 'changelist')},
                {'title': 'Course Resources', 'url': self.get_model_url(CourseResource, 'changelist')},
                {'title': 'Course Comments', 'url': self.get_model_url(CourseComments, 'changelist')},
            )},

            {'title': 'User Management', 'menus': (
                {'title': 'User Info', 'url': self.get_model_url(UserProfile, 'changelist')},
                {'title': 'User Verification', 'url': self.get_model_url(EmailVerifyRecord, 'changelist')},
                {'title': 'User Courses', 'url': self.get_model_url(UserCourse, 'changelist')},
                {'title': 'User Favorites', 'url': self.get_model_url(UserFavorite, 'changelist')},
                {'title': 'User Messages', 'url': self.get_model_url(UserMessage, 'changelist')},
            )},

            {'title': 'System Management', 'menus': (
                {'title': 'User Inquiries', 'url': self.get_model_url(UserAsk, 'changelist')},
                {'title': 'Homepage Banners', 'url': self.get_model_url(Banner, 'changelist')},
                {'title': 'User Groups', 'url': self.get_model_url(Group, 'changelist')},
                {'title': 'User Permissions', 'url': self.get_model_url(Permission, 'changelist')},
                {'title': 'Log Records', 'url': self.get_model_url(Log, 'changelist')},
            )},
        )


# 创建admin的管理类,这里不再是继承admin，而是继承object
class EmailVerifyRecordAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['code', 'email', 'send_type']
    # 配置筛选字段
    list_filter = ['code', 'email', 'send_type', 'send_time']


# 创建banner的管理类
class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# 将model与admin管理器进行关联注册
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

# 将Xadmin全局管理器与我们的view绑定注册。
xadmin.site.register(views.BaseAdminView, BaseSetting)

# 将头部与脚部信息进行注册:
xadmin.site.register(views.CommAdminView, GlobalSettings)
