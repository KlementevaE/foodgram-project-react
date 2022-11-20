from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'first_name')


admin.site.register(User, UserAdmin)
