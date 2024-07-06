from django.contrib import admin
from .models import PricingConfig, DayPricingConfig, PricingConfigLog
from .forms import PricingConfigForm, DayPricingConfigForm

class DayPricingConfigInline(admin.TabularInline):
    model = DayPricingConfig
    form = DayPricingConfigForm
    extra = 1

class PricingConfigAdmin(admin.ModelAdmin):
    form = PricingConfigForm
    inlines = [DayPricingConfigInline]
    list_display = ('config_name', 'is_active')
    actions = ['activate_configs', 'deactivate_configs']

    def activate_configs(self, request, queryset):
        queryset.update(is_active=True)
    activate_configs.short_description = "Activate selected configs"

    def deactivate_configs(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_configs.short_description = "Deactivate selected configs"

admin.site.register(PricingConfig, PricingConfigAdmin)
admin.site.register(PricingConfigLog)
