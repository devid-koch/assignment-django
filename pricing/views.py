import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PricingConfig
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP


@csrf_exempt
def calculate_price(request):
    if request.method == 'POST':
        try:
            ride_details = json.loads(request.body)
            distance = Decimal(ride_details.get('distance'))
            time = Decimal(ride_details.get('time'))
            waiting_time = Decimal(ride_details.get('waiting_time'))
            date = ride_details.get('date')
            day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%a')

            config = PricingConfig.objects.filter(days_of_week=day_of_week, is_active=True).first()
            if not config:
                return JsonResponse({'error': 'No active pricing configuration found for the given day.'}, status=404)

            if distance <= config.distance_base_kms:
                base_price = config.distance_base_price
            else:
                base_price = config.distance_base_price + (distance - config.distance_base_kms) * config.distance_additional_price

            time_multiplier = Decimal('1.00')
            if time > Decimal('1.00'):
                time_multiplier = config.time_multiplier_factor

            waiting_charges = max(Decimal('0.00'), waiting_time - config.initial_waiting_time) * (config.waiting_charges / Decimal('3.00'))

            # Calculate final price
            final_price = (base_price * time_multiplier) + waiting_charges

            # Round the final price to two decimal places
            final_price = final_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            return JsonResponse({'price': str(final_price)})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except (TypeError, ValueError) as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
