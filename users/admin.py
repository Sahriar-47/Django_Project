from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)
    actions = ['make_coadmin']

    def make_coadmin(self, request, queryset):
        queryset.update(role='co-admin')
    make_coadmin.short_description = 'Grant Co-Admin Privileges'
