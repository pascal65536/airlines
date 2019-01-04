from django.contrib import admin
from airlines.models import Airlines


class AirlinesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Airlines)
