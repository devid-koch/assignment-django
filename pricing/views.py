import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PricingConfig, DayPricingConfig
from decimal import Decimal, ROUND_HALF_UP

@csrf_exempt
def calculate_price(request):
    if request.method == 'POST':
        try:
            ride_details = json.loads(request.body)
            distance = Decimal(ride_details.get('distance'))
            time = Decimal(ride_details.get('time'))
            waiting_time = Decimal(ride_details.get('waiting_time'))
            day = ride_details.get('day').capitalize()
            config_name = ride_details.get('config_name')

            config = PricingConfig.objects.filter(config_name=config_name, is_active=True).first()
            if not config:
                return JsonResponse({'error': 'No active pricing configuration found for the given configuration name.'}, status=404)

            day_config = config.day_configs.filter(day_of_week=day).first()
            if not day_config:
                return JsonResponse({'error': f'No pricing configuration found for {day}.'}, status=404)

            if distance <= day_config.distance_base_kms:
                base_price = day_config.distance_base_price
            else:
                base_price = day_config.distance_base_price + (distance - day_config.distance_base_kms) * day_config.distance_additional_price

            time_multiplier = Decimal('1.00')
            if time > Decimal('1.00'):
                time_multiplier = day_config.time_multiplier_factor

            waiting_charges = max(Decimal('0.00'), waiting_time - day_config.initial_waiting_time) * (day_config.waiting_charges / Decimal('3.00'))

            final_price = (base_price * time_multiplier) + waiting_charges

            final_price = final_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            return JsonResponse({
                'price': str(final_price),
                'details': {
                    'distance': str(distance),
                    'time': str(time),
                    'waiting_time': str(waiting_time),
                    'day': day,
                    'config_name': config_name
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except (TypeError, ValueError) as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
