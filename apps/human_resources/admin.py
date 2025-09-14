from django.contrib import admin
from .models import (
    Person, 
    Organization, 
    Location, 
    OrganizationalUnit, 
    JobPosition, 
    PersonInfoContact, 
    Employee, 
    Schedule, 
    EmployeeSchedule, 
    LeaveType, 
    LeaveRequest
)

# Register your models here.
admin.site.register(Person)
admin.site.register(Organization)
admin.site.register(Location)
admin.site.register(OrganizationalUnit)
admin.site.register(JobPosition)
admin.site.register(PersonInfoContact)
admin.site.register(Employee)
admin.site.register(Schedule)
admin.site.register(EmployeeSchedule)
admin.site.register(LeaveType)
admin.site.register(LeaveRequest)