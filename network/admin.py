from django.contrib import admin
from .models import User, Posts, Profile

# Register your models here.
admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Profile)
