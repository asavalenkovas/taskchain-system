from django.contrib import admin
from .models import Project, Task, Machine


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ("name", "machine", "status", "priority", "order", "due_date")
    show_change_link = True


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "display_tasks", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    inlines = [TaskInline]


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "machine", "status", "priority", "order", "due_date")
    list_filter = ("status", "priority", "project", "machine")
    list_editable = ("status", "priority", "order")
    search_fields = ("name", "description", "part_code")
    autocomplete_fields = ("project", "machine", "depends_on")
    fieldsets = (
        ("Pagrindine informacija", {
            "fields": ("project", "name", "description", "part_code")
        }),
        ("Vykdymo informacija", {
            "fields": ("machine", "quantity", "depends_on")
        }),
        ("Valdymas", {
            "fields": ("status", "priority", "order", "due_date")
        }),
    )


class MachineAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name")


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Machine, MachineAdmin)