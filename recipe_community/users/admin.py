from django.contrib import admin

from .models import User

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')
