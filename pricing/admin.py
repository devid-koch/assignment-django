
from django.contrib import admin
from .models import PricingConfig, PricingConfigLog
from .forms import PricingConfigForm

class PricingConfigAdmin(admin.ModelAdmin):
    form = PricingConfigForm
    list_display = ('days_of_week', 'distance_base_price', 'distance_additional_price', 'time_multiplier_factor', 'waiting_charges', 'is_active')
    actions = ['activate_configs', 'deactivate_configs']

    def activate_configs(self, request, queryset):
        queryset.update(is_active=True)
    activate_configs.short_description = "Activate selected configs"

    def deactivate_configs(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_configs.short_description = "Deactivate selected configs"

admin.site.register(PricingConfig, PricingConfigAdmin)
admin.site.register(PricingConfigLog)
