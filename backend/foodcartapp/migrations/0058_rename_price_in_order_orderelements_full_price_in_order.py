# Generated by Django 3.2 on 2022-08-23 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0057_rename_restaurant_order_cooking_restaurant'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderelements',
            old_name='price_in_order',
            new_name='full_price_in_order',
        ),
    ]
