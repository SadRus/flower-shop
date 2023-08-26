from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from flower_shop.settings import YKASSA_SHOP_ID, YKASSA_SECRET_KEY
from shop.models import Bouquet, Store, Client, Order, Consultation
from shop.forms import OrderForm, ConsultationForm

from yookassa import Configuration, Payment
import uuid


def index(request):
    bouquets = Bouquet.objects.all()
    stores = Store.objects.all()
    context = {
        'bouquets': bouquets,
        'stores': stores,
        'form': ConsultationForm(),
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
    else:
        form = ConsultationForm()
        result = False
    context = {
        'form': form,
        'result': result,
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
                        "value": "100.00",
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": "https://starburgerito.ru/payment_result/"
                    },
                    "capture": True,
                    "description": "Оплата заказа #123"
                },
                uuid.uuid4()
            )

            return render(request, 'payment.html', {'payment': payment})

    else:
        form = OrderForm()
    context = {
        'form': form,
    }
    return render(request, 'order.html', context)


def payment_result(request):
    result = True  # or False

    context = {
        'result': result,
        'order': 1,
    }
    return render(request, 'payment_result.html', context)


def quiz(request):
    return render(request, 'quiz.html')


def quiz_step(request):
    event = request.POST.get('event')
    return render(request, 'quiz-step.html')


def result(request):
    return render(request, 'result.html')
