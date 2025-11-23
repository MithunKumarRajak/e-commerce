from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account
from django.utils.html import format_html
from .models import UserProfile
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'phone_number', 'is_admin', 'is_staff',
        'is_active', 'is_superadmin'
    )

    list_display_links = ('email', 'username')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)  # - for descending and its a tuple not list

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# user profile admin panel
class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(obj.profile_picture.url))
        return '-'

    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
