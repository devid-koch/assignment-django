from django.db import models
class PricingConfig(models.Model):
    config_name = models.CharField(max_length=50, default="")
    is_active = models.BooleanField(default=True)

class DayPricingConfig(models.Model):
    pricing_config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE, related_name='day_configs')
    day_of_week = models.CharField(max_length=10)
    distance_base_price = models.DecimalField(max_digits=10, decimal_places=2)
    distance_base_kms = models.DecimalField(max_digits=5, decimal_places=2)
    distance_additional_price = models.DecimalField(max_digits=10, decimal_places=2)
    time_multiplier_factor = models.DecimalField(max_digits=4, decimal_places=2)
    waiting_charges = models.DecimalField(max_digits=5, decimal_places=2)
    initial_waiting_time = models.DecimalField(max_digits=5, decimal_places=2)

class PricingConfigLog(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE)
    changed_by = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    old_value = models.JSONField(default=dict)
    new_value = models.JSONField(default=dict)  # Default value as an empty dictionary
