from django.contrib import admin
from .models import Acount
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    # waa field-yada page-ka (ACCOUNT) marka aad dhexgashid kusoo muqanaya.
    list_display = ('email', 'first_name', 'last_name','last_login', 'date_joined', 'is_staff', 'is_admin')
    list_filter = ('is_admin',)

    # waa field-yada (UPDATE-page) kasoo muqanaya.
    fieldsets = (
        (None, {'fields': ('email', 'password','first_name','last_name', 'country')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff','is_active')}),
    )

    # waa field-yada page-ka (ADD ACCOUNT+)
    add_fieldsets = (
        ('New account', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('username',)#search par
    ordering = ('-date_joined',) #qaabka ay isugu xigan.
    filter_horizontal = ()       #Attribute-kan waxaa badanaa loo isticmaalaa field-yada leh (ManyToMany).


admin.site.register(Acount, UserAdmin)