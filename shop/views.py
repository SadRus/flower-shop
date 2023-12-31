import json
import uuid

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from yookassa import Configuration, Payment

from flower_shop.settings import YKASSA_SHOP_ID, YKASSA_SECRET_KEY, ADMIN_TG_CHAT_ID, TG_TOKEN
from shop.models import Bouquet, BouquetComponent, Event, Store, Client, Order, Consultation
from shop.forms import OrderForm, ConsultationForm
from shop.bot import TelegramNotifier


def index(request):
    bouquets = Bouquet.objects.all().order_by('?')
    stores = Store.objects.all()
    context = {
        'bouquets': bouquets,
        'stores': stores,
    }
    return render(request, 'index.html', context=context)


def card(request, id):
    bouquet = get_object_or_404(Bouquet, id=id)
    context = {
        'bouquet': bouquet,
    }
    return render(request, 'card.html', context=context)


def catalog(request):
    bouquets = Bouquet.objects.all()
    context = {
        'bouquets': bouquets
    }
    return render(request, 'catalog.html', context=context)


def consultation(request):
    result = None
    name = None
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            Consultation.objects.create(
                name=name,
                phone=phone,
            )
            result = True
            bot = TelegramNotifier(TG_TOKEN, ADMIN_TG_CHAT_ID)
            bot.send_notify(f'У вас новая заявка на консультацию: {name}, {phone}')
    else:
        form = ConsultationForm()
        result = False
    context = {
        'form': form,
        'result': result,
        'name': name,
    }
    return render(request, 'consultation.html', context)


def order(request, id):
    bouquet = get_object_or_404(Bouquet, pk=id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            timeslot = form.cleaned_data['timeslot']

            client, _ = Client.objects.get_or_create(name=name, phone=phone)

            order = Order.objects.create(
                client=client,
                address=address,
                bouquet=bouquet,
                timeslot=timeslot,
            )

            Configuration.account_id = YKASSA_SHOP_ID
            Configuration.secret_key = YKASSA_SECRET_KEY

            payment = Payment.create(
                {
                    "amount": {
                        "value": order.bouquet.price,
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": f"https://starburgerito.ru/payment_result?order_id={order.id}"
                    },
                    "capture": True,
                    "description": f"Оплата заказа #{order.id}"
                },
                uuid.uuid4()
            )

            order.payment_id = json.loads(payment.json())['id']
            order.save()

            context = {
                'payment': payment,
                'order': order
            }
            return render(request, 'payment.html', context)

    else:
        form = OrderForm()
    context = {
        'form': form,
    }
    return render(request, 'order.html', context)


def payment_result(request):
    check_payment_result = False
    customer_order = get_object_or_404(Order, id=request.GET.get('order_id'))
    order_payment_id = customer_order.payment_id

    Configuration.account_id = YKASSA_SHOP_ID
    Configuration.secret_key = YKASSA_SECRET_KEY
    payment = json.loads((Payment.find_one(order_payment_id)).json())
    if payment['status'] == 'succeeded':
        check_payment_result = True
        customer_order.is_paid = True
        customer_order.save()
        bot = TelegramNotifier(TG_TOKEN, ADMIN_TG_CHAT_ID)
        bot.send_notify(f'Оплачен новый заказ № {customer_order.id}')

    context = {
        'result': check_payment_result,
        'order': customer_order,
    }

    return render(request, 'payment_result.html', context)


def quiz(request):
    context = {
        'events': Event.objects.all()
    }
    return render(request, 'quiz.html', context=context)


def quiz_step(request):
    event = request.GET.get('event')
    response = render(request, 'quiz-step.html')
    response.set_cookie(key='event_id', value=event)
    return response


def result(request):
    price = request.GET.get('price')
    event_id = request.COOKIES['event_id']

    event_bouquets = Bouquet.objects.filter(event=int(event_id))
    if not event_bouquets:
        event_bouquets = Bouquet.objects.all()

    if price == "1000":
        quiz_bouquet = event_bouquets.filter(price__lt=1000) \
            .order_by('?') \
            .first()
    elif price == "5000":
        quiz_bouquet = event_bouquets.filter(price__gte=1000, price__lt=5000) \
            .order_by('?') \
            .first()
    elif price == "5000+":
        quiz_bouquet = event_bouquets.filter(price__gte=5000) \
            .order_by('?') \
            .first()
    else:
        quiz_bouquet = event_bouquets.order_by('?').first()

    stores = Store.objects.all()

    context = {
        'bouquet': quiz_bouquet,
        'stores': stores,
    }

    response = render(request, 'result.html', context=context)
    response.delete_cookie('event')
    return response
