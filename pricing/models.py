from django.db import models
from django.contrib.auth.models import User

class PricingConfig(models.Model):
    DAYS_OF_WEEK = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]

    distance_base_price = models.DecimalField(max_digits=10, decimal_places=2)
    distance_base_kms = models.DecimalField(max_digits=5, decimal_places=2)
    distance_additional_price = models.DecimalField(max_digits=10, decimal_places=2)
    time_multiplier_factor = models.DecimalField(max_digits=5, decimal_places=2)
    waiting_charges = models.DecimalField(max_digits=10, decimal_places=2)
    initial_waiting_time = models.IntegerField(default=3)  # in minutes
    days_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Config for {self.get_days_of_week_display()}"

class PricingConfigLog(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    change_description = models.TextField()

    def __str__(self):
        return f"Log for {self.config} at {self.timestamp}"
