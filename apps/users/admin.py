from django.contrib import admin
from .models import CustomUser, GroupProxy

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(GroupProxy)