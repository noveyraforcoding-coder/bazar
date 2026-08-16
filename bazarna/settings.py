import os
import firebase_admin
from firebase_admin import credentials
from pathlib import Path
from dotenv import load_dotenv

from django.contrib.messages import constants as messages
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

# ==============================================================================
# 1. BASE DIRECTORY & ENVIRONMENT VARIABLES
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

# ==============================================================================
# 2. CORE SETTINGS
# ==============================================================================
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-change-in-production')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
ROOT_URLCONF = 'bazarna.urls'
WSGI_APPLICATION = 'bazarna.wsgi.application'
SITE_ID = 1

# ==============================================================================
# 3. SECURITY & CORS SETTINGS
# ==============================================================================
SESSION_COOKIE_AGE = 1209600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# ==============================================================================
# 4. APPLICATIONS & MIDDLEWARE
# ==============================================================================
INSTALLED_APPS = [
    'modeltranslation',
    'cloudinary_storage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # Third-Party Apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'corsheaders',

    # Local Apps
    'accounts',
    'store',
    'support',
    'merchant_panel',
    'supervisor',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'bazarna._sys_monitor.SystemIntegrityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'accounts.middleware.BanMiddleware',
    'accounts.middleware.MerchantApprovalMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# ==============================================================================
# 5. TEMPLATES
# ==============================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.site_settings',
                'support.context_processors.support_tickets_processor',
                'accounts.context_processors.mobile_app_detector',
                'store.context_processors.active_promo_popup',
                'store.context_processors.global_country_context',
            ],
        },
    },
]

# ==============================================================================
# 6. DATABASE & CACHING
# ==============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache_table',
    }
}

# ==============================================================================
# 7. INTERNATIONALIZATION & TIME
# ==============================================================================
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = 'ar'

LANGUAGES = (
    ('ar', _('Arabic')),
    ('en', _('English')),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ar'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = 'Africa/Cairo'
DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'P'
DATETIME_FORMAT = 'Y-m-d P'

# ==============================================================================
# 8. AUTHENTICATION & ALLAUTH
# ==============================================================================
AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.EmailPhoneUsernameBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Allauth Settings (django-allauth >= 65.x)
ACCOUNT_ADAPTER = 'accounts.adapters.MyAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'accounts.adapters.MySocialAccountAdapter'
ACCOUNT_RATE_LIMITS = {}
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_FORMS = {'signup': 'accounts.forms.MySocialSignupForm'}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'key': '',
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'VERIFIED_EMAIL': True,
    }
}

# ==============================================================================
# 9. DJANGO REST FRAMEWORK
# ==============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# ==============================================================================
# 10. STATIC & MEDIA FILES
# ==============================================================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.getenv('CLOUDINARY_URL')
}
if os.getenv('CLOUDINARY_URL'):
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ==============================================================================
# 11. THIRD-PARTY & EXTRA CONFIGURATIONS
# ==============================================================================

# Paymob Payment Gateway (Egypt)
PAYMOB_API_KEY = os.getenv('PAYMOB_API_KEY')
PAYMOB_INTEGRATION_ID_CARD = os.getenv('PAYMOB_INTEGRATION_ID_CARD')
PAYMOB_INTEGRATION_ID_WALLET = os.getenv('PAYMOB_INTEGRATION_ID_WALLET')
PAYMOB_IFRAME_ID = os.getenv('PAYMOB_IFRAME_ID')

# Fawaterk Payment Gateway (Multi-region)
FAWATERK_API_KEY = os.getenv('FAWATERK_API_KEY')
FAWATERK_SUCCESS_URL = os.getenv('FAWATERK_SUCCESS_URL', 'https://your-domain.com/my-orders/')
FAWATERK_WEBHOOK_URL = os.getenv('FAWATERK_WEBHOOK_URL', 'https://your-domain.com/payment/callback/')

# Upload Size Limits (20 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520
FILE_UPLOAD_MAX_MEMORY_SIZE = 20971520

# Message Tags (Bootstrap Integration)
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ==============================================================================
# 12. FIREBASE CLOUD MESSAGING
# ==============================================================================
FIREBASE_KEY_PATH = os.path.join(BASE_DIR, 'firebase-key.json')
firebase_cred_json = os.environ.get('FIREBASE_CREDENTIALS_JSON')

if not firebase_admin._apps:
    try:
        if firebase_cred_json:
            import json
            cred_dict = json.loads(firebase_cred_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        elif os.path.exists(FIREBASE_KEY_PATH):
            cred = credentials.Certificate(FIREBASE_KEY_PATH)
            firebase_admin.initialize_app(cred)
        else:
            print("WARNING: Firebase credentials not found. Notifications will not work.")
    except Exception as e:
        print(f"WARNING: Failed to initialize Firebase: {e}")

# ==============================================================================
# 13. DEFAULT AUTO FIELD
# ==============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'