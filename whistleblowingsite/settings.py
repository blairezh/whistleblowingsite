"""
Django settings for whistleblowingsite project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import django_heroku
import dj_database_url

from pathlib import Path
import django


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4&94zqgd0qrf&7xi)e=g@(!gc-a_cmlrk++(q60sp*a7lqzt63'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'a-08-3e91aaebfb2c.herokuapp.com']

SITE_ID = 1 #identifies which site we are using for login 
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login.apps.LoginConfig', 
    'storages',
    "django.contrib.sites",
    "allauth", #allows other forms of authentication
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    
]


#specify variable for social account provider
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [ #from when google credential was created
            "profile",
            "email", 
        ],
        "AUTH_PARAMS": {"access_type": "online"},
        'APP': {
        'CLIENT_ID': os.environ.get('GOOGLE_OAUTH_CLIENT_ID'),
        'SECRET': os.environ.get('GOOGLE_OAUTH_SECRET'),
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # 'whistleblowingsite.middleware.DynamicSiteMiddleware',
]

ROOT_URLCONF = 'whistleblowingsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'whistleblowingsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if "DYNO" in os.environ and not "CI" in os.environ:
    DATABASES = {
    #    "default": {
    #         "ENGINE": "django.db.backends.postgresql",
    #         "NAME": "d2kip5ta1daa7b",
    #         "USER": "qzjjkbarorajem",
    #         "PASSWORD": "083fdfa0178875986a8e055e649531431ee079923c6a92773fb729c19be7980d",
    #         "HOST": "ec2-34-236-199-229.compute-1.amazonaws.com",
    #         "PORT": "5432",
    #     }
        
        "default": dj_database_url.config(
            #default='postgres://rgpazisydbriod:754dc0a3685fb9a29c962b376f0576de023ae257f119c2f93453a44a8d3ec7d3@ec2-52-6-117-96.compute-1.amazonaws.com:5432/dao2pqt1ft1n89',
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        ),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#AWS S3 config
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID') 
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY') 

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_FILE_OVERWRITE = False
AWS_LOCATION = 'static'


# STORAGES = {  
#     "default": { #for media files
#         "BACKEND": "storages.backends.s3.S3Storage",
#     },
    

# }

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend", #using standard django backend
    "allauth.account.auth_backends.AuthenticationBackend" #and allauth backend
)

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

#configure static files
#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_ROOT = BASE_DIR / "staticfiles"  #collect static files
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

django_heroku.settings(locals(), staticfiles=False, test_runner=False)