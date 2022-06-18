from django.contrib import admin

from .models import *
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ("first_name", "last_name", "username", "email", "phonenumber", "date_joined", "is_approved", )
    list_display = ("first_name", "last_name", "email", "date_joined")
    list_filter = ("date_joined", )
    search_fields = ("first_name__startswith", )

    class Meta:
        ordering = ("date_joined")