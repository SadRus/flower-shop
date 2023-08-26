from django.shortcuts import render
from shop.models import Bouquet, BouquetComponent, Event, Store


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


def order(request):
    return render(request, 'order.html')


def order_step(request):
    print(request)
    return render(request, 'order-step.html')


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

    event = Event.objects.get(id=event_id)
    if event.name == 'Без повода':
        event_bouquets = Bouquet.objects.all()
    else:
        event_bouquets = Bouquet.objects.filter(event=int(event_id))

    match price:
        case "1000":
            quiz_bouquet = event_bouquets.filter(price__lt=1000) \
                                         .order_by('?') \
                                         .first()
        case "5000":
            quiz_bouquet = event_bouquets.filter(price__gte=1000, price__lt=5000) \
                                         .order_by('?') \
                                         .first()
        case "5000+":
            quiz_bouquet = event_bouquets.filter(price__gte=5000) \
                                         .order_by('?') \
                                         .first()
        case "None":
            quiz_bouquet = event_bouquets.order_by('?').first()

    bouquet_components = BouquetComponent.objects.filter(bouquet=quiz_bouquet)

    context = {
        'bouquet': quiz_bouquet,
        'bouquet_components': bouquet_components,
    }

    response = render(request, 'result.html', context=context)
    response.delete_cookie('event')
    return response
