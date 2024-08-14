from django.contrib import admin

from donate.admin import DonateAdmin
from users.models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')
    order_by = ('username',)
    inlines = (DonateAdmin,)

@admin.register(EmailVerification)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created']
    readonly_fields = ['created',]
    order_by = ['-created',]
