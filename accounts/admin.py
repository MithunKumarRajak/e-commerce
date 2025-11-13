from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account
# Register your models here.


class DisplayOnAdminPanel(UserAdmin):
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


admin.site.register(Account, DisplayOnAdminPanel)
