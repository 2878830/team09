from datetime import datetime

from DjangoUeditor.models import UEditorField
from django.db import models
from organization.models import CourseOrg, Teacher


# 课程信息表
# Course Information Table
class Course(models.Model):
    DEGREE_CHOICES = (
        ("cj", u"primary"),
        ("zj", u"intermediate"),
        ("gj", u"advanced")
    )
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u"Organization", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=u"Lecture", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"Course Name")
    desc = models.CharField(max_length=300, verbose_name=u"Course Description")
    # TextField允许我们不限制长度的输入，以后替换为富文本的，可以输入文字还可以修改
    # TextField allows us to input without length limitation. Will be replaced with rich text editor later, which can input text and modify
    # 修改imagepath，不能传y m,不能加斜杠，相对路径，相对于配置的media_root
    # Modify imagepath, cannot use y m, cannot add slash, relative path relative to configured media_root
    detail = UEditorField(verbose_name=u"Course Details", width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    is_banner = models.BooleanField(default=False, verbose_name=u"Is Banner")
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=2, verbose_name=u"Difficulty")
    # 使用分钟做后台记录(存储最小单位)前台转换 
    # Using minutes for backend records (minimum storage unit) frontend conversion
    learn_times = models.IntegerField(default=0, verbose_name=u"Learning Time(Minutes)")
    # 保存学习人数:点击开始学习才算
    # Save number of learners: only count when clicking "Start Learning"
    students = models.IntegerField(default=0, verbose_name=u"Students")
    fav_nums = models.IntegerField(default=0, verbose_name=u"Favorites")
    you_need_know = models.CharField(max_length=300, default=u"Study hard and improve every day", verbose_name=u"Preparation")
    teacher_tell = models.CharField(max_length=300, default=u"Come,on!", verbose_name=u"Teacher's Advice")
    image = models.ImageField(
        upload_to="courses/%Y/%m",
        verbose_name=u"Cover",
        max_length=100)
    # 保存点击量，点进页面就算 
    # Save number of clicks, only count when clicking
    click_nums = models.IntegerField(default=0, verbose_name=u"Clicks")
    category = models.CharField(max_length=20, verbose_name=u"Course Category", default=u"Back-end Development")
    tag = models.CharField(max_length=15, verbose_name=u"Course Tags", default=u"")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add Time")

    class Meta:
        verbose_name = u"Course"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 章节 chapter
class Lesson(models.Model):
    # 因为一个课程对应很多章节。所以在章节表中将课程设置为外键。
    # 作为一个字段来让我们可以知道这个章节对应那个课程
    # Since one course corresponds to many chapters, set course as foreign key in chapter table.
    # As a field to let us know which course this chapter corresponds to
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u"Course")
    name = models.CharField(max_length=100, verbose_name=u"Chapter Name")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add Time")

    class Meta:
        verbose_name = u"Chapter"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》Course chapter >> {1}'.format(self.course, self.name)


# 章节视频 video
class Video(models.Model):
    # 因为一个章节对应很多视频。所以在视频表中将章节设置为外键。
    # Since one chapter corresponds to many videos, set lesson as foreign key in video table.    
    # 作为一个字段来存储让我们可以知道这个视频对应哪个章节.
    # As a field to let us know which video this chapter corresponds to.
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=u"Chapter")
    url = models.CharField(max_length=1000, default="https://space.bilibili.com/1565906988", verbose_name=u"Video Address")
    name = models.CharField(max_length=100, verbose_name=u"Video Name")
    # 使用分钟做后台记录(存储最小单位)前台转换 
    # Using minutes for backend records (minimum storage unit) frontend conversion
    learn_times = models.IntegerField(default=0, verbose_name=u"Learning Time(Minutes)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add Time")

    class Meta:
        verbose_name = u"Video"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}Chapter of video >> {1}'.format(self.lesson, self.name)


# 课程资源 resources
class CourseResource(models.Model):
    # 因为一个课程对应很多资源。所以在课程资源表中将课程设置为外键。
    # 作为一个字段来让我们可以知道这个资源对应那个课程
    # Since one course corresponds to many resources, the course is set as a foreign key in the course resource table.
    # This field is used to indicate which course this resource belongs to.
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u"Course")
    name = models.CharField(max_length=100, verbose_name=u"Name")
    # 这里定义成文件类型的field，后台管理系统中会直接有上传的按钮。
    # FileField也是一个字符串类型，要指定最大长度。
    # This field is defined as a file type, which will provide a direct upload button in the backend management system.
    # FileField is essentially a string type and requires a maximum length to be specified.
    download = models.FileField(
        upload_to="course/resource/%Y/%m",
        verbose_name=u"Download",
        max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add Time")

    class Meta:
        verbose_name = u"Course Resource"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》course resources: {1}'.format(self.course, self.name)
