from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import *
# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    #fields = ("first_name", "last_name", "username", "password", "email", "phonenumber", "date_joined", "is_approved", )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_approved', )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Contact info', {'fields': ('email', 'phonenumber')}),)
  
    list_display = ("first_name", "last_name", "email", "date_joined")
    list_filter = ("date_joined", )
    search_fields = ("first_name__startswith", )
    ordering = ("-date_joined", )