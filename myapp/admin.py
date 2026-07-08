from django.contrib import admin

from myapp.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
