from django.contrib import admin
from airlines.models import Airlines


class AirlinesAdmin(admin.ModelAdmin):
    list_filter = ('status', 'country',)
    list_display = ('title', 'created', 'changed', 'deleted',)
    empty_value_display = '-empty-'
    show_full_result_count = True


admin.site.register(Airlines, AirlinesAdmin)
