from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# 用户信息 user information
class UserProfile(AbstractUser):
   
    GENDER_CHOICES = (
        ("male", u"male"),
        ("female", u"female")
    )
    # 昵称 nick name
    nick_name = models.CharField(max_length=50, verbose_name=u"Name", default="")
    # 生日，可以为空 birthday is null
    birthday = models.DateField(verbose_name=u"birth", null=True, blank=True)
    # 性别 只能男或女，默认女 gender 
    gender = models.CharField(
        max_length=6,
        verbose_name=u"gender",
        choices=GENDER_CHOICES,
        default="female")
    # 地址 address
    address = models.CharField(max_length=100, verbose_name="address", default="")
    # 电话 telephone
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=u"phone")
    # 头像 默认使用default.png image
    image = models.ImageField(
        upload_to="image/%Y/%m",
        default=u"image/default.png",
        max_length=100,
        verbose_name=u"image"
    )

    # 后台栏目名 verbose_name
    class Meta:
        verbose_name = "User Information"
        verbose_name_plural = verbose_name

    # 重载__str__方法，打印实例会打印username，username为继承自AbstractUser loading from django.contrib.auth.models import AbstractUser
    def __str__(self):
        return self.username

    # 获取用户未读消息的数量 unread message
    def unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(has_read=False, user=self.id).count()


# 邮箱验证记录表 email verification record
class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (
        ("register", u"Register"),
        ("forget", u"Find password"),
        ("update_email", u"Change email"),
    )
    code = models.CharField(max_length=20, verbose_name=u"Verification code")
    # 未设置null = true blank = true 默认不可为空 set null = true blank = true
    email = models.EmailField(max_length=50, verbose_name=u"Email")
    send_type = models.CharField(choices=SEND_CHOICES, max_length=20, verbose_name=u"Verification Type")
    # 这里的now得去掉(),不去掉会根据编译时间。而不是根据实例化时间。 now = datetime.now()
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u"Send Time")

    class Meta:
        verbose_name = "Email Verification Code"
        verbose_name_plural = verbose_name

    # 重载str方法使后台不再直接显示object str method 
    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


# 轮播图 banner
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"Title")
    image = models.ImageField(
        upload_to="banner/%Y/%m",
        verbose_name=u"Carousel Image",
        max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"Access Address")
    # 默认index很大靠后。想要靠前修改index值。 index = models.IntegerField(default=100, verbose_name=u"Sequence")
    index = models.IntegerField(default=100, verbose_name=u"Sequence")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"Add Time")

    class Meta:
        verbose_name = u"Carousel Image"
        verbose_name_plural = verbose_name

    # 重载__str__方法使后台不再直接显示object str method
    def __str__(self):
        return '{0}(Rank{1})'.format(self.title, self.index)
