from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = list(UserAdmin.fieldsets) + [
        (
            'Información adicional',
            {
                'fields': ('bio', 'avatar'),
            },
        ),
    ]

admin.site.register(CustomUser, CustomUserAdmin)

