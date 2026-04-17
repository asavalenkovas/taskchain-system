from django.contrib import admin
from .models import EmployeeProfile


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "machine")
    list_filter = ("role", "machine")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    autocomplete_fields = ("user", "machine")
