# Generated by Django 4.2.4 on 2023-08-26 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_consultation_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='идентификатор юкасса'),
        ),
    ]
