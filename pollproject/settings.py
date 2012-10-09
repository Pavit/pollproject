# Django settings for pollproject project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

import dj_database_url
import os

if bool(os.environ.get('HEROKU_LOCAL_DEV', False)):
	DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',   ##Local DB is sqlite3 because setting up postgresql is annoying
		'NAME': 'pollproject_local_db',
		'HOST': '',
		'PORT': '',
		'USER': '',
		'PASSWORD': '',
		}
	}
	# Separate Facebook apps for local development / heroku
	FACEBOOK_APP_ID = '343120432448964'
	FACEBOOK_API_SECRET= '0809eaae9cae32bf4f3574f47c0fca5e'
	RECAPTCHA_PUBLIC_KEY = '6Lek5dYSAAAAAIY02lNb3e05q6oowiTH9M6LzjFK'
	RECAPTCHA_PRIVATE_KEY = '6Lek5dYSAAAAAKoaOHtnU4HQL36hpxGCcP5XW6MD'
else:
	DATABASES = {'default': dj_database_url.config(default=os.environ["DATABASE_URL"])}
	FACEBOOK_APP_ID = '406831919365032'
	FACEBOOK_API_SECRET= '924a5a01f43de7d991cd1c17edf4469b'
	RECAPTCHA_PUBLIC_KEY = '6Ld45dYSAAAAABWB2fissbEYq5kb7dsHhH58L'
	RECAPTCHA_PRIVATE_KEY = '6Ld45dYSAAAAAB2J60uDKRYhvcpbKzdIPcCyRdWb'


TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'dj0c$4h8cvw4b%ia(igup5-t*0(*%@o)qyr4^i47ys1^hjhui^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS	=	(
'django.template.loaders.filesystem.Loader',
'django.template.loaders.app_directories.Loader',
#		'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
'django.contrib.auth.context_processors.auth',
'django.core.context_processors.debug',
'django.core.context_processors.i18n',
'django.core.context_processors.media',
'django.core.context_processors.static',
'django.core.context_processors.tz',
'django.contrib.messages.context_processors.messages',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pollproject.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pollproject.wsgi.application'


ROOT_PATH = os.path.dirname(__file__)

TEMPLATE_DIRS = (
	os.path.join(ROOT_PATH,"templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'poll',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'core',
    'facepy',
    'social_auth',
    'captcha',
    "tagging_autocomplete_tagit",
    'tagging',
)

RECAPTCHA_PUBLIC_KEY = '6Ld45dYSAAAAABWB2fissbEYq5kb7dsHhH58L-cd'
RECAPTCHA_PRIVATE_KEY = '6Ld45dYSAAAAAB2J60uDKRYhvcpbKzdIPcCyRdWb'

#TAGGING_AUTOCOMPLETE_JS_BASE_URL = '/static/js/jquery-tag-it/'


LOGIN_URL          = '/login-form/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/login-error/'

#SOCIAL_AUTH_USER_MODEL = 'core.CustomUser'
FACEBOOK_EXTENDED_PERMISSIONS = [
	'email','friends_likes','user_about_me',
	'user_birthday', 'friends_birthday', 'friends_about_me',
	'user_location', 'friends_location','user_relationships','friends_relationships',
	'friends_education_history','user_education_history','user_interests',
	'friends_interests','user_relationship_details','friends_relationship_details','user_religion_politics',
	'friends_religion_politics',
]

AUTHENTICATION_BACKENDS = (
'social_auth.backends.facebook.FacebookBackend',
'django.contrib.auth.backends.ModelBackend',
)

TEST_FACEBOOK_USER = 'testuser1@gmail.com'
TEST_FACEBOOK_PASSWORD = 'testuser1'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

