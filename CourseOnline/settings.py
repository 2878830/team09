import os
import sys


from apps import operation, courses, users
from extra_apps import  DjangoUeditor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))


SECRET_KEY = '+1nruftzf9)mi3mb!0_wpsmw=pne(717j(xszq_ghmap2024zq'


DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition 
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)

# app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users', 
    'courses',  
    'operation', 
    'organization', 
    'xadmin', 
    'crispy_forms',  
    'captcha', 
    'pure_pagination', 
    'DjangoUeditor', 
]


AUTH_USER_MODEL = "users.UserProfile"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'CourseOnline.urls'


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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'team09three$db_course_online',  
        'USER': 'team09three', 
        'PASSWORD': '123456it',  
        'HOST': 'team09three.mysql.pythonanywhere-services.com'

    }
}


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


USE_TZ = True

#  (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
if os.getenv('DJANGO_PRODUCTION', 'False') == 'True':
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp-relay.brevo.com"  # Brevo 的 SMTP 服务器
EMAIL_PORT = 587  # 使用 TLS 加密
EMAIL_USE_TLS = True  # 需要开启 TLS 连接
EMAIL_USE_SSL = False  # 不使用 SSL（因为 TLS 和 SSL 只能选一个）

EMAIL_HOST_USER = "888628001@smtp-brevo.com"  # 你的 Brevo SMTP 登录用户名
EMAIL_HOST_PASSWORD = "mgqxJdMpyUAGFbEj"  # 你的 Brevo SMTP 密码
DEFAULT_FROM_EMAIL = "tkc11147@gmail.com"  # 改成你的 Gmail 邮箱（用于发件）



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
