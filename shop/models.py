from django.core.validators import MinValueValidator
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Event(models.Model):
    name = models.CharField(
        'Событие',
        max_length=30,
    )

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"

    def __str__(self):
        return f"{self.name}"


class Component(models.Model):
    name = models.CharField(
        'Название компонента',
        max_length=50,
    )

    class Meta:
        verbose_name = "Компонент букета"
        verbose_name_plural = "Компоненты букета"

    def __str__(self):
        return f"{self.name}"


class Timeslot(models.Model):
    name = models.CharField(
        'Период доставки',
        max_length=50,
    )

    class Meta:
        verbose_name = "Период доставки"
        verbose_name_plural = "Периоды доставки"

    def __str__(self):
        return f"{self.name}"


class Consultation(models.Model):
    name = models.CharField(
        'Имя клиента',
        max_length=250,
    )
    phone = models.CharField(
        'Телефон',
        max_length=13,
    )
    is_processed = models.BooleanField(
        'Консультация оказана?',
        default=False,
    )

    class Meta:
        verbose_name = "Заявка на консультацию"
        verbose_name_plural = "Заявки на консультацию"

    def __str__(self):
        return f"От {self.name}"


class Bouquet(models.Model):
    name = models.CharField(
        'Название букета',
        max_length=250,
    )
    price = models.PositiveIntegerField(
        'Цена',
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
    )
    components = models.ManyToManyField(
        Component,
        through='BouquetComponent',
        related_name='bouquets',
        verbose_name='Компоненты',
    )
    image = models.ImageField(
        'Изображение букета',
        upload_to='flowers/',
    )
    event = models.ForeignKey(
        Event,
        verbose_name='К какому событию',
        related_name='bouquets',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    width = models.PositiveIntegerField(
        'Ширина',
        null=True,
        blank=True,
    )
    height = models.PositiveIntegerField(
        'Высота',
        null=True,
        blank=True,
    )


    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"

    def __str__(self):
        return f"{self.name}"


class BouquetComponent(models.Model):
    bouquet = models.ForeignKey(
        Bouquet,
        verbose_name='Букет',
        on_delete=models.CASCADE,
    )
    component = models.ForeignKey(
        Component,
        verbose_name='Компонент',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        'Количество',
        validators=[MinValueValidator(1)],
    )


class Client(models.Model):
    name = models.CharField(
        'Имя клиента',
        max_length=250,
    )
    phone = PhoneNumberField(
        'Телефон',
    )
    email = models.EmailField(
        'E-mail',
        max_length=100,
        null=True,
        blank=True,
    )


class Order(models.Model):
    client = models.ForeignKey(
        Client,
        verbose_name='Клиент',
        related_name='orders',
        null=True,
        on_delete=models.SET_NULL,
    )
    address = models.EmailField(
        'Адрес',
        max_length=250,
    )
    bouquet = models.ForeignKey(
        Bouquet,
        verbose_name='Букет',
        related_name='orders',
        null=True,
        on_delete=models.SET_NULL,
    )
    timeslot = models.ForeignKey(
        Timeslot,
        verbose_name='Период времени для доставки',
        related_name='orders',
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.id} от {self.client.name}"


class Store(models.Model):
    address = models.CharField(
        'Адрес',
        max_length=250,
    )
    phone = PhoneNumberField(
        'Телефон',
    )
