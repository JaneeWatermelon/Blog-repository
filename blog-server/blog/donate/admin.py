from django.contrib import admin

from donate.models import Donate
from users.models import User


class DonateAdmin(admin.TabularInline):
    model = Donate
    list_display = ['id', 'user', 'price']
    order_by = ['id']
    extra = 0
