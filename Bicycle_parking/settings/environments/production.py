import os
import dj_database_url
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
S3_BUCKET = os.environ.get('S3_BUCKET')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
MAPS_API_KEY = os.environ.get('MAPS_API_KEY')

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_CUSTOM_DOMAIN = os.environ.get('STATIC_URL')

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=3000',
}

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# please fill out these settings for your own local machine!
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bike_parking_toronto',
        'USER': os.getenv('BIKE_DB_USER', 'postgres'),
        'PASSWORD': os.getenv('BIKE_DB_PW', 'postgres'),
        'HOST': os.getenv('BIKE_DB_HOST', 'localhost'),
        'PORT': '5432',
    }
}

# note: BIKE_DB_* variables replace $DATABASE_URL to support
# multiple database access
# Update database configuration with $DATABASE_URL.
# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)

# define the database routers; these objects route requests passed to the django
# routines to update or access a table defined as a model class in python
# to the appropriate database

DATABASE_ROUTERS = ['bicycleparking.Routers.DefaultRouting']

# my_project/settings.py
LOGIN_REDIRECT_URL = '/moderate_unapproved'                    
