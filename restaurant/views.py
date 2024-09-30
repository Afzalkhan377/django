from django.shortcuts import render
import random 
import random
import time
from django.utils import timezone
from datetime import timedelta
def main(request):
    return render(request, 'restaurant/main.html')



from django.shortcuts import render

def order(request):
    menu_items = [
        {'name': 'chicken over rice', 'price': 10.99},
        {'name': 'lamb over rice', 'price': 10.99},
        {'name': 'combo over rice', 'price': 11.99},
        {'name': '6pc buffalo hot wings', 'price': 10.99},
    ]

    daily_special = random.choice(menu_items)

    context = {
        'menu_items': menu_items,
        'daily_special': daily_special
    }

    return render(request, 'restaurant/order.html', context)



def confirmation(request):
    if request.method == 'POST':
        customer_name = request.POST.get('name')
        customer_phone = request.POST.get('phone')
        customer_email = request.POST.get('email')
        instructions = request.POST.get('instructions')

        ordered_items = []
        total_price = 0

   
        for item in ['chicken_over_rice', 'lamb_over_rice', 'combo_over_rice', 'daily_special']:
            if request.POST.get(item):
              
                price = float(request.POST.get(f'{item}_price'))
                quantity = int(request.POST.get(f'{item}_qty'))
                item_total = price * quantity

               
                ordered_items.append({
                    'name': request.POST.get(item),
                    'price': price,
                    'quantity': quantity,
                    'item_total': item_total
                })
                total_price += item_total

        selected_toppings = []
        for topping in ['white_sauce', 'bbq_sauce', 'mint_sauce']:
            if request.POST.get(topping):
                topping_quantity = int(request.POST.get(f'{topping}_qty'))
                topping_price = float(request.POST.get(f'{topping}_price'))
                topping_total = topping_price * topping_quantity
                selected_toppings.append({
                    'name': request.POST.get(topping),
                    'quantity': topping_quantity,
                    'topping_total': topping_total
                })
                total_price += topping_total

        current_time = timezone.localtime(timezone.now())
        random_minutes = random.randint(30, 60)
        ready_time = current_time + timedelta(minutes=random_minutes)

   
        context = {
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'instructions': instructions,
            'ordered_items': ordered_items,
            'selected_toppings': selected_toppings,
            'total_price': total_price,
            'ready_time': ready_time.strftime('%I:%M %p')
        }

        return render(request, 'restaurant/confirmation.html', context)