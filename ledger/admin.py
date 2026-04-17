from django.contrib import admin
from .models import Block


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("index", "event_type", "created_at")
    list_filter = ("event_type", "created_at")
    search_fields = ("event_type", "hash", "prev_hash")
    readonly_fields = ("index", "created_at", "prev_hash", "hash", "event_type", "event_data")

    fieldsets = (
        ("Pagrindine informacija", {"fields": ("index", "event_type", "created_at")} ),
        ("Hash duomenys", {"fields": ("prev_hash", "hash")} ),
        ("Ivykio turinys", {"fields": ("event_data",)} ),
    )
