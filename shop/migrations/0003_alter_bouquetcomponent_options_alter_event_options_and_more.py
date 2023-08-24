# Generated by Django 4.2.4 on 2023-08-24 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_client_options_alter_store_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bouquetcomponent',
            options={'verbose_name': 'Компонент в букете', 'verbose_name_plural': 'Компоненты в букете'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Событие для букетов', 'verbose_name_plural': 'События для букетов'},
        ),
        migrations.AlterUniqueTogether(
            name='bouquetcomponent',
            unique_together={('bouquet', 'component')},
        ),
    ]