from django.contrib.auth import get_user_model

DJANGO_ADMIN_USER = 'admin'
DJANGO_ADMIN_PASS = 'password'
DJANGO_ADMIN_EMAIL = 'admin@example.com'

User = get_user_model()  # get the currently active user model,

User.objects.filter(username=DJANGO_ADMIN_USER).exists() or \
        User.objects.create_superuser(DJANGO_ADMIN_USER, DJANGO_ADMIN_EMAIL, DJANGO_ADMIN_PASS)
