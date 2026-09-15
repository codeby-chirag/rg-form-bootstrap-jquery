from django.contrib import admin

from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'fullname',
        'email',
        'calculate_age',
        'number',
        'gender',
        'country',
    )
    # list_display_links = ["fullname",]
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'number')
    list_filter = ('gender', 'country')
    
    
