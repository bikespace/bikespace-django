import dj_database_url

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

#please fill out these settings for your own local machine!
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bike_parking_toronto',
        'USER': os.getenv ('BIKE_DB_USER', 'postgres'),
        'PASSWORD': os.getenv ('BIKE_DB_PW', ''),
        'HOST': os.getenv ('BIKE_DB_HOST', 'postgres'),
        'PORT': '5432',
    },
    'geospatial' : {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'intersection',
        'USER': os.getenv ('BIKE_DB_USER', 'postgres'),
        'PASSWORD': os.getenv ('BIKE_DB_PW', ''),
        'HOST': os.getenv ('BIKE_DB_HOST', 'postgres'),
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

DATABASE_ROUTERS = [ 'bicycleparking.Routers.GeoSpatialRouting', 
                     'bicycleparking.Routers.DefaultRouting' ]
