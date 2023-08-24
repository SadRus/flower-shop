from django.shortcuts import render
from shop.models import Bouquet


def index(request):
    bouquets = Bouquet.objects.all()
    context = {
        'bouquets': bouquets
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


def order(request):
    return render(request, 'order.html')


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
