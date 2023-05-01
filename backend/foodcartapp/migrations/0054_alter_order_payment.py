# Generated by Django 3.2 on 2022-08-11 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0053_order_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(blank=True, choices=[('CARD', 'Электронно'), ('CASH', 'Наличностью')], db_index=True, max_length=4, null=True, verbose_name='Способ оплаты'),
        ),
    ]