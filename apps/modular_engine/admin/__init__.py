from django.contrib import admin
from apps.modular_engine.models.module import Module
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'version', 'installed_date')
    search_fields = ('name', 'slug')
    list_filter = ('status',)




class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_groups')

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])

    get_groups.short_description = 'Roles'

# Unregister default UserAdmin
admin.site.unregister(User)
# Register custom UserAdmin
admin.site.register(User, CustomUserAdmin)