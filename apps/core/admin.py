from django.contrib import admin
from .models import ChangeLog, User, Person, ContactInfo, EmergencyContactInfo

# Register your models here.
admin.site.register(ChangeLog)
admin.site.register(User)
admin.site.register(Person)
admin.site.register(ContactInfo)
admin.site.register(EmergencyContactInfo)