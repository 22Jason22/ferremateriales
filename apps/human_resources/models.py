"""ZZZ"""
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey
from django.utils import timezone
from django.conf import settings

# pylint: disable=no-member


class Person(models.Model):
    """ZZZ"""

    SEX_CHOICES = [
        (True, _("Man")),
        (False, _("Woman"))
    ]
    MARITAL_STATUS_CHOICES = [
        (1, _("Single")),
        (2, _("Married")),
        (3, _("Divorced")),
        (4, _("Widowed"))
    ]
    first_name = models.CharField(
        _("First Name"),
        max_length=25,
        help_text=_("The person's first name.")
    )
    middle_name = models.CharField(
        _("Middle Name"),
        max_length=25,
        null=True,
        blank=True,
        help_text=_("The person's middle name (optional).")
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=25,
        help_text=_("The person's last name.")
    )
    second_last_name = models.CharField(
        _("Second Last Name"),
        max_length=25,
        null=True,
        blank=True,
        help_text=_("The person's second last name (optional).")
    )
    birth_date = models.DateField(
        _("Birth Date"),
        null=True,
        blank=True,
        help_text=_("The person's date of birth.")
    )
    sex = models.BooleanField(
        _("Sex"),
        choices=SEX_CHOICES,
        default=True,
        help_text=_("The person's biological sex.")
    )
    is_venezuelan = models.BooleanField(
        _("Venezuelan"),
        default=True,
        help_text=_("Indicates if the person is Venezuelan.")
    )
    identity_number = models.CharField(
        _("Identity Number"),
        max_length=8,
        help_text=_("The person's national identity number.")
    )
    marital_status = models.PositiveSmallIntegerField(
        _("Marital Status"),
        choices=MARITAL_STATUS_CHOICES,
        help_text=_("The person's marital status.")
    )
    user = models.OneToOneField(
        "users.CustomUser",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="person_profile",
        help_text=_("The associated user account for this person.")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Indicates if the person record is active.")
    )

    class Meta:
        """ZZZ"""
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        unique_together = [
            (
                "is_venezuelan",
                "identity_number"
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        """ZZZ"""
        return reverse("Person_detail", kwargs={"pk": self.pk})


class Organization(models.Model):
    """ZZZ"""

    business_name = models.CharField(
        _("Name"),
        max_length=100,
        unique=True,
        help_text=_("The official name of the organization.")
    )
    rif = models.CharField(
        _("RIF"),
        max_length=10,
        default="",
        help_text=_("Tax identification number of the organization.")
    )
    fiscal_address = models.CharField(
        _("Fiscal Address"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Fiscal address of the organization.")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Indicates if the organization is currently active.")
    )

    class Meta:
        """Meta definition for Organization."""
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __str__(self):
        return f"{self.business_name}"

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of Organization."""
        return reverse("Organization_detail", kwargs={"pk": self.pk})


class Location(models.Model):
    """
    Represents a physical location associated with an organization.
    """
    organization = models.ForeignKey(
        Organization,
        verbose_name=_("Organization"),
        on_delete=models.CASCADE,
        related_name='locations',
        help_text=_("The organization this location belongs to.")
    )
    name = models.CharField(
        _("Location Name"),
        max_length=255,
        help_text=_("Name of the location.")
    )
    address = models.CharField(
        _("Address"),
        max_length=100,
        help_text=_("Physical address of the location.")
    )
    state = models.CharField(
        _("State"),
        max_length=255,
        help_text=_("State of operation.")
    )

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return f"{self.name} ({self.organization.business_name})"


class OrganizationalUnit(models.Model):
    """ZZZ"""

    name = models.CharField(
        _("Name"),
        max_length=25,
        unique=True,
        help_text=_("The name of the organizational unit.")
    )
    organization = models.ForeignKey(
        "Organization",
        verbose_name=_("Organization"),
        on_delete=models.CASCADE,
        related_name="organizational_units",
        help_text=_("The organization this unit belongs to.")
    )
    parent_organization = models.ForeignKey(
        "self",
        verbose_name=_("Parent Organization"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="child_units",
        help_text=_("The parent organizational unit, if any.")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Indicates if the organizational unit is currently active.")
    )

    class Meta:
        """Meta definition for OrganizationalUnit."""
        verbose_name = _("Organizational Unit")
        verbose_name_plural = _("Organizational Units")

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of OrganizationalUnit."""
        return reverse("OrganizationalUnit_detail", kwargs={"pk": self.pk})


class JobPosition(models.Model):
    """ZZZ"""

    title = models.CharField(
        _("Title"),
        max_length=50,
        unique=True,
        help_text=_("The title of the job position.")
    )
    description = models.TextField(
        _("Description"),
        null=True,
        blank=True,
        help_text=_("A detailed description of the job responsibilities.")
    )
    organizational_unit = models.ForeignKey(
        "OrganizationalUnit",
        verbose_name=_("Organizational Unit"),
        on_delete=models.CASCADE,
        related_name="job_positions",
        help_text=_("The organizational unit where this job position is located.")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Indicates if the job position is currently active.")
    )

    class Meta:
        """Meta definition for JobPosition."""
        verbose_name = _("Job Position")
        verbose_name_plural = _("Job Positions")

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of JobPosition."""
        return reverse("JobPosition_detail", kwargs={"pk": self.pk})


class PersonInfoContact(models.Model):
    """
    Stores contact information for a person.
    """
    state_province = models.CharField(
        _("State/Province"),
        max_length=255,
        help_text=_("State or province of residence.")
    )
    municipality = models.CharField(
        _("Municipality"),
        max_length=255,
        help_text=_("Municipality of residence.")
    )
    parish = models.CharField(
        _("Parish"),
        max_length=255,
        help_text=_("Parish of residence.")
    )
    postal_code = models.CharField(
        _("Postal Code"),
        max_length=10,
        help_text=_("Postal code of the area.")
    )
    personal_address = models.CharField(
        _("Personal Address"),
        max_length=100,
        help_text=_("Detailed personal address.")
    )
    local_phone_prefix = models.CharField(
        _("Local Phone Prefix"),
        max_length=4,
        null=True,
        blank=True,
        help_text=_("Prefix for local phone number.")
    )
    local_phone_number = models.CharField(
        _("Local Phone Number"),
        max_length=10,
        null=True,
        blank=True,
        help_text=_("Local phone number.")
    )
    mobile_phone_prefix = models.CharField(
        _("Mobile Phone Prefix"),
        max_length=4,
        help_text=_("Prefix for mobile phone number.")
    )
    mobile_phone_number = models.CharField(
        _("Mobile Phone Number"),
        max_length=10,
        help_text=_("Mobile phone number.")
    )
    person = models.OneToOneField(
        Person,
        verbose_name=_("Person"),
        on_delete=models.CASCADE,
        related_name='contact_info',
        help_text=_("Related person for this contact information.")
    )

    class Meta:
        verbose_name = _("Person Contact Info")
        verbose_name_plural = _("Person Contact Info")

    def __str__(self):
        return f"Contact Info for {self.person.first_name} {self.person.last_name}"


class Employee(models.Model):
    """ZZZ"""

    organization = models.ForeignKey(
        Organization,
        verbose_name=_("Organization"),
        on_delete=models.CASCADE,
        related_name="employees",
        help_text=_("The organization the employee belongs to.")
    )
    organizational_unit = ChainedForeignKey(
        "OrganizationalUnit",
        chained_field="organization",
        chained_model_field="organization",
        show_all=False,
        auto_choose=True,
        verbose_name=_("Organizational Unit"),
        on_delete=models.CASCADE,
        related_name="employees_in_unit",
        help_text=_("The organizational unit the employee works in.")
    )
    job_position = ChainedForeignKey(
        "JobPosition",
        chained_field="organizational_unit",
        chained_model_field="organizational_unit",
        show_all=False,
        auto_choose=True,
        verbose_name=_("Job Position"),
        on_delete=models.CASCADE,
        related_name="employees_in_position",
        help_text=_("The employee's job position.")
    )
    hire_date = models.DateField(
        _("Hire Date"),
        help_text=_("The date the employee was hired.")
    )
    person = models.OneToOneField(
        "Person",
        verbose_name=_("Person"),
        on_delete=models.CASCADE,
        related_name="employee_record",
        help_text=_("The personal information of the employee.")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Indicates if the employee record is active.")
    )

    class Meta:
        """Meta definition for Employee."""
        db_table = 'employee'
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name} - {self.job_position.title}"

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of Employee."""
        return reverse("Employee_detail", kwargs={"pk": self.pk})


class Schedule(models.Model):
    """
    Model representing an employee work schedule.
    """
    name = models.CharField(
        _("Name"),
        max_length=100,
        unique=True
    )
    start_time = models.TimeField(
        _("Start Time")
    )
    end_time = models.TimeField(
        _("End Time")
    )
    days_of_week = models.CharField(
        _("Days of Week"),
        max_length=50,
        help_text=_("Comma-separated days, e.g., Mon,Tue,Wed,Thu,Fri")
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True
    )
    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True
    )

    class Meta:
        """
        Meta configuration for the Schedule model.
        """
        db_table = "hr_schedules"
        verbose_name = _("Schedule")
        verbose_name_plural = _("Schedules")

    def __str__(self):
        return self.name


class EmployeeSchedule(models.Model):
    """
    Model linking an employee to a specific work schedule.
    """
    employee = models.ForeignKey(
        Employee,
        verbose_name=_("Employee"),
        on_delete=models.CASCADE
    )
    schedule = models.ForeignKey(
        Schedule,
        verbose_name=_("Schedule"),
        on_delete=models.CASCADE
    )
    start_date = models.DateField(
        _("Start Date"),
        default=timezone.now
    )
    end_date = models.DateField(
        _("End Date"),
        null=True,
        blank=True
    )
    is_current = models.BooleanField(
        _("Is Current"),
        default=True,
        help_text=_("Indicates if this is the employee's current active schedule.")
    )
    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True
    )

    class Meta:
        """
        Meta configuration for the EmployeeSchedule model.
        """
        db_table = "hr_employee_schedules"
        verbose_name = _("Employee Schedule")
        verbose_name_plural = _("Employee Schedules")
        unique_together = (
            'employee',
            'schedule',
            'start_date'
        )

    def __str__(self):
        return f"{self.employee} - {self.schedule.name}"


class LeaveType(models.Model):
    """
    Model representing different types of employee leave.
    """
    name = models.CharField(
        _("Name"),
        max_length=100,
        unique=True
    )
    description = models.TextField(
        _("Description"),
        null=True,
        blank=True
    )
    is_paid = models.BooleanField(
        _("Is Paid"),
        default=True
    )
    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True
    )

    class Meta:
        """
        Meta configuration for the LeaveType model.
        """
        db_table = "hr_leave_types"
        verbose_name = _("Leave Type")
        verbose_name_plural = _("Leave Types")

    def __str__(self):
        return self.name


class LeaveRequest(models.Model):
    """
    Model representing an employee's leave request.
    """
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('cancelled', _('Cancelled')),
    ]

    employee = models.ForeignKey(
        Employee,
        verbose_name=_("Employee"),
        on_delete=models.CASCADE
    )
    leave_type = models.ForeignKey(
        LeaveType,
        verbose_name=_("Leave Type"),
        on_delete=models.CASCADE
    )
    start_date = models.DateField(
        _("Start Date"),
        default=timezone.now
    )
    end_date = models.DateField(
        _("End Date"),
        default=timezone.now
    )
    reason = models.TextField(
        _("Reason"),
        null=True,
        blank=True
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Approved By"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True
    )

    class Meta:
        """
        Meta configuration for the LeaveRequest model.
        """
        db_table = "hr_leave_requests"
        verbose_name = _("Leave Request")
        verbose_name_plural = _("Leave Requests")

    def __str__(self):
        return f"{self.employee} - {self.leave_type.name} ({self.status})"