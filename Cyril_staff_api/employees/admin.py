from django.contrib import admin
from .models import Manager, Intern, Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['street_address', 'city', 'state', 'country']
    search_fields = ['street_address', 'city', 'state', 'country']
    list_filter = ['country', 'state']

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'department', 'hire_date', 'is_active']
    list_filter = ['department', 'is_active', 'has_company_card', 'hire_date']
    search_fields = ['first_name', 'last_name', 'email', 'department']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Employment Details', {'fields': ('hire_date', 'salary', 'department', 'is_active')}),
        ('Company Information', {'fields': ('has_company_card',), 'classes': ('collapse',)}),
        ('Address Information', {'fields': ('address',)}),
        ('System Information', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Intern)
class InternAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'mentor', 'internship_end_date', 'is_active']
    list_filter = ['is_active', 'internship_end_date', 'mentor']
    search_fields = ['first_name', 'last_name', 'email', 'mentor__first_name', 'mentor__last_name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Employment Details', {'fields': ('hire_date', 'salary', 'is_active')}),
        ('Internship Information', {'fields': ('mentor', 'internship_end_date')}),
        ('Address Information', {'fields': ('address',)}),
        ('System Information', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
