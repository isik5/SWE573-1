from django.contrib import admin
from accounts.models import UserInfo, Consumation, Sport

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Consumation)
admin.site.register(Sport)