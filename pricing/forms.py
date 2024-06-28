
from django import forms
from .models import PricingConfig

class PricingConfigForm(forms.ModelForm):
    class Meta:
        model = PricingConfig
        fields = ['distance_base_price', 'distance_base_kms', 'distance_additional_price', 'time_multiplier_factor', 'waiting_charges', 'initial_waiting_time', 'days_of_week', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
