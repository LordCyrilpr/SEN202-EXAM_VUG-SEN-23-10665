from django.db import models


class Address(models.Model):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}"


class StaffBase(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_role(self):
        return "Staff Member"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Manager(StaffBase):
    department = models.CharField(max_length=100)
    has_company_card = models.BooleanField(default=True)

    def get_role(self):
        return f"Manager - {self.department}"

    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Managers"


class Intern(StaffBase):
    mentor = models.ForeignKey(
        Manager, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='interns'
    )
    internship_end_date = models.DateField()

    def get_role(self):
        mentor_name = self.mentor.full_name if self.mentor else "No mentor assigned"
        return f"Intern - Mentored by {mentor_name}"

    class Meta:
        verbose_name = "Intern"
        verbose_name_plural = "Interns"
