from django.contrib import admin
from .models import Post,Topic,Comment,Like_Dislike,Reply,CustomUser
from django.contrib.auth.admin import UserAdmin
from django.conf import settings

admin.site.register(Topic)
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like_Dislike)
admin.site.register(Reply)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name','profile_picture', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
admin.site.register(CustomUser, CustomUserAdmin)

