from django import forms
from .models import PricingConfig, DayPricingConfig

class DayPricingConfigForm(forms.ModelForm):
    class Meta:
        model = DayPricingConfig
        fields = ['day_of_week', 'distance_base_price', 'distance_base_kms', 'distance_additional_price', 
                  'time_multiplier_factor', 'waiting_charges', 'initial_waiting_time']

class PricingConfigForm(forms.ModelForm):
    class Meta:
        model = PricingConfig
        fields = ['config_name', 'is_active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            self.fields[f'{day.lower()}_config'] = forms.ModelChoiceField(
                queryset=DayPricingConfig.objects.filter(day_of_week=day),
                required=False
            )
