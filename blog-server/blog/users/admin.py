from django.contrib import admin

from donate.admin import DonateAdmin
from users.models import EmailVerification, User

@admin.action(description="Сменить пароль пользователя")
def change_password(modeladmin, request, queryset):
    for user in queryset:
        user.set_password('Janeeplay123')
        user.save()
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')
    order_by = ('username',)
    inlines = (DonateAdmin,)
    actions = (change_password,)

@admin.register(EmailVerification)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created']
    readonly_fields = ['created',]
    order_by = ['-created',]
