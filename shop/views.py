from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from shop.models import Bouquet, Store, Client, Order
from shop.forms import OrderForm


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
    return render(request, 'consultation.html')


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

            return HttpResponseRedirect(f'link-to-pay-with-{order.id}')
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
