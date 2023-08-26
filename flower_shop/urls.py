"""
URL configuration for flower_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from shop import views
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('card', views.card, name='card'),
    path('catalog', views.catalog, name='catalog'),
    path('consultation', views.consultation, name='consultation'),
    path('order/<int:id>', views.order, name='order'),
    path('payment_result', views.payment_result, name='payment_result'),
    path('quiz', views.quiz, name='quiz'),
    path('quiz-step', views.quiz_step, name='quiz-step'),
    path('result', views.result, name='result'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
