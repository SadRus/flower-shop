from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from shop.models import Bouquet, Store
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
            #subject = form.cleaned_data["subject"]
            print('form valid, creating user & order')
            return HttpResponseRedirect("/thanks/")
    else:
        form = OrderForm()
    context = {
        'form': form,
    }
    return render(request, 'order.html', context)


def order_step(request):
    print(request)
    return render(request, 'order-step.html')


def quiz(request):
    return render(request, 'quiz.html')


def quiz_step(request):
    event = request.POST.get('event')
    return render(request, 'quiz-step.html')


def result(request):
    return render(request, 'result.html')
