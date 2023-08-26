import uuid

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from yookassa import Configuration, Payment

from flower_shop.settings import YKASSA_SHOP_ID, YKASSA_SECRET_KEY, ADMIN_TG_CHAT_ID, TG_TOKEN
from shop.models import Bouquet, Store, Client, Order, Consultation
from shop.forms import OrderForm, ConsultationForm
from shop.bot import TelegramNotifier


def index(request):
    bouquets = Bouquet.objects.all()
    stores = Store.objects.all()
    context = {
        'bouquets': bouquets,
        'stores': stores,
    }
    return render(request, 'index.html', context=context)


def card(request):
    return render(request, 'card.html')


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
                        "return_url": "https://starburgerito.ru/payment_result"
                    },
                    "capture": True,
                    "description": f"Оплата заказа #{order.id}"
                },
                uuid.uuid4()
            )

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

    result = True  # or False
    order = 1
    # here we should set is_paid field of Order to True if result is successes
    # and here we should notify admin by telegram abut new order
    if result:
        bot = TelegramNotifier(TG_TOKEN, ADMIN_TG_CHAT_ID)
        bot.send_notify(f'Оплачен новый заказ № {order}')
        bot.send_notify(request.GET)

    context = {
        'result': result,
        'order': order,
    }

    return render(request, 'payment_result.html', context)


def quiz(request):
    return render(request, 'quiz.html')


def quiz_step(request):
    event = request.POST.get('event')
    return render(request, 'quiz-step.html')


def result(request):
    return render(request, 'result.html')
