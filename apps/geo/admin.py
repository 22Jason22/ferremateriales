from django.contrib import admin
from .models import Country, Federalstate, Municipality, Parish, PostalCode, LandlinePrefix

# Register your models here.
admin.site.register(Country)
admin.site.register(Federalstate)
admin.site.register(Municipality)
admin.site.register(Parish)
admin.site.register(PostalCode)
admin.site.register(LandlinePrefix)