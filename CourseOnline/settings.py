import os
import sys

# 项目路径
from apps import operation, courses, users
from extra_apps import  DjangoUeditor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 将这两个目录添加到环境变量
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# 项目秘钥
SECRET_KEY = '+1nruftzf9)mi3mb!0_wpsmw=pne(717j(xszq_ghmap2024zq'

# 调试模式
DEBUG = True

# 允许的主机
ALLOWED_HOSTS = ['*']

# Application definition 注册我们的app
# 设置邮箱和用户名均可登录
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)

# 注册app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',  # 用户管理模块
    'courses',  # 课程管理模块
    'operation',  #
    'organization',  # 机构管理模块
    'xadmin',  # 后台管理系统
    'crispy_forms',  # 表单
    'captcha',  # 验证码
    'pure_pagination',  # 分页
    'DjangoUeditor',  # 富文本编辑器
]

# 此处重载是为了使我们的UserProfile生效
AUTH_USER_MODEL = "users.UserProfile"

# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 根路由
ROOT_URLCONF = 'CourseOnline.urls'

# 前端模板文件
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.i18n",
                'django.template.context_processors.media',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'CourseOnline.wsgi.application'

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_course_online',  # 数据库名称
        'USER': 'root',  # 账号
        'PASSWORD': '123456',  # 密码
        'HOST': '127.0.0.1'

    }
}

# 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True

# 数据库存储使用时间，True时间会被存为UTC的时间
USE_TZ = True

#  (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# 发送邮件的setting设置
EMAIL_HOST = "smtp.qq.com"
EMAIL_PORT = 587   
EMAIL_HOST_USER = "1301510900@qq.com"
EMAIL_HOST_PASSWORD = "erurhmhvjlusjijf"
EMAIL_USE_TLS = True
EMAIL_FROM = "1301510900@qq.com"

# 设置我们上传文件的路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
