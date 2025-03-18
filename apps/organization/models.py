# coding : utf-8
from datetime import datetime

from django.db import models


# 城市字典 cities
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"City")
    # 城市描述：备用不一定展示出来 description about the city
    desc = models.CharField(max_length=200, verbose_name=u"Description")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add Time")

    class Meta:
        verbose_name = u"City"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 课程机构 organizations
class CourseOrg(models.Model):
    ORG_CHOICES = (
        ("pxjg", u"Training Organization"),
        ("gx", u"University"),
        ("gr", u"Personal"),
    )
    name = models.CharField(max_length=50, verbose_name=u"Organization Name")
    # 机构描述，后面会替换为富文本展示 description about the organization
    desc = models.TextField(verbose_name=u"Organization Description")
    # 机构类别: category of the organization
    category = models.CharField(max_length=20, choices=ORG_CHOICES, verbose_name=u"Organization Category", default="pxjg")
    tag = models.CharField(max_length=10, default=u"Famous schools", verbose_name=u"Organization Tag")
    click_nums = models.IntegerField(default=0, verbose_name=u"Clicks")
    fav_nums = models.IntegerField(default=0, verbose_name=u"Favorites")
    image = models.ImageField(
        upload_to="org/%Y/%m",
        verbose_name=u"Logo",
        max_length=100)
    address = models.CharField(max_length=150, verbose_name=u"Address")
    # 一个城市可以有很多课程机构，通过将city设置外键，变成课程机构的一个字段 a city has many organizations
    # 可以让我们通过机构找到城市 find cities through organizations
    city = models.ForeignKey(CityDict, on_delete=models.CASCADE, verbose_name=u"City")
    # 当学生点击学习课程，找到所属机构，学习人数加1 click nums add 1
    students = models.IntegerField(default=0, verbose_name=u"Students")
    # 当发布课程就加1 add1
    course_nums = models.IntegerField(default=0, verbose_name=u"Courses")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add Time")

    class Meta:
        verbose_name = u"Course Organization"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "course institution: {0}".format(self.name)


# 讲师
class Teacher(models.Model):
    # 一个机构会有很多老师，所以我们在讲师表添加外键并把课程机构名称保存下来 a teacher has many organizations
    # 可以使我们通过讲师找到对应的机构 find organizations through teachers
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u"Organization")
    name = models.CharField(max_length=50, verbose_name=u"Teacher Name")
    work_years = models.IntegerField(default=0, verbose_name=u"Work Years")
    work_company = models.CharField(max_length=50, verbose_name=u"Company")
    work_position = models.CharField(max_length=50, verbose_name=u"Position")
    age = models.IntegerField(default=18, verbose_name=u"Age")
    points = models.CharField(max_length=50, verbose_name=u"Features")
    click_nums = models.IntegerField(default=0, verbose_name=u"Clicks")
    fav_nums = models.IntegerField(default=0, verbose_name=u"Favorites")
    image = models.ImageField(
        default='',
        upload_to="teacher/%Y/%m",
        verbose_name=u"Image",
        max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add Time")

    class Meta:
        verbose_name = u"Teacher"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "Teacher of[{0}]: {1}".format(self.org, self.name)
