from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext

from .models import Todo, User


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (gettext('Personal Info'), {'fields': ('name', )}),
        (
            gettext('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (gettext('Important dates'), {'fields': ('last_login', )})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.site_header = 'ToDo Administration'
admin.site.site_title = 'ToDo Administration'

admin.site.register(User, UserAdmin)
admin.site.register(Todo)
