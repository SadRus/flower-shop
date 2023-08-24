from django.contrib import admin

from .models import Event, Component, Timeslot, Consultation, Bouquet, BouquetComponent, Client, Order, Store

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    pass


@admin.register(Timeslot)
class TimeslotAdmin(admin.ModelAdmin):
    pass


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    pass


class RestaurantMenuItemInline(admin.TabularInline):
    model = BouquetComponent
    extra = 0

@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    inlines = [
        RestaurantMenuItemInline
    ]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass