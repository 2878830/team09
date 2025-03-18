from datetime import datetime

from courses.models import Course
from django.db import models
# 引入我们CourseComments所需要的外键models foreingkey
from users.models import UserProfile


# 我要学习表单 form about forms
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"Name")
    mobile = models.CharField(max_length=11, verbose_name=u"Mobile Number")
    course_name = models.CharField(max_length=50, verbose_name=u"Course Name")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add Time")

    class Meta:
        verbose_name = u"User Consultation"
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'user: {0} telephone number: {1}'.format(self.name, self.mobile)


# 课程评论 form about forms
class CourseComments(models.Model):
    # 会涉及两个外键: 1. 用户， 2. 课程。import进来 Course user import
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u"Course")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=u"User")
    comments = models.CharField(max_length=250, verbose_name=u"Comment")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Comment Time")

    class Meta:
        verbose_name = u"Course Comments"
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'user({0})Comments on《{1}》:'.format(self.user, self.course)


# 课程,机构,讲师的收藏 cource,org,teacher
class UserFavorite(models.Model):
    # 会涉及四个外键。用户，课程，机构，讲师import Course UserProfile
    TYPE_CHOICES = (
        (1, u"course"),
        (2, u"course institution"),
        (3, u"Lecturer")
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=u"User")
    # 直接保存用户的id. save users id
    fav_id = models.IntegerField(default=0)
    # 表明收藏的是哪种类型。 type about collections
    fav_type = models.IntegerField(
        choices=TYPE_CHOICES,
        default=1,
        verbose_name=u"Collection Type")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Comment Time")

    class Meta:
        verbose_name = u"User Favorites"
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'user({0})collected{1} '.format(self.user, self.fav_type)


# 用户消息表 user message
class UserMessage(models.Model):
    # 因为我们的消息有两种:发给全员和发给某一个用户。 send to all or send to one user
    # 所以如果使用外键，每个消息会对应要有用户。很难实现全员消息。 if user=0,send to all users. if user!=0,send to one user
    # 机智版 为0发给所有用户，不为0就是发给用户的id if user=0,send to all users. if user!=0,send to one user
    user = models.IntegerField(default=0, verbose_name=u"Accept Users")
    message = models.CharField(max_length=500, verbose_name=u"Message")

    # 是否已读: 布尔类型 BooleanField False未读,True表示已读 if user=0,send to all users. if user!=0,send to one user
    has_read = models.BooleanField(default=False, verbose_name=u"Have you read it")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add Time")

    class Meta:
        verbose_name = u"User Messages"
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'user({0})receives {1} '.format(self.user, self.message)


# 用户课程表 user course
class UserCourse(models.Model):
    # 会涉及两个外键: 1. 用户， 2. 课程。import进来 Course UserProfile
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u"Course")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=u"User")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add Time")

    class Meta:
        verbose_name = u"User Course"
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'user({0})learn{1} '.format(self.user, self.course)
