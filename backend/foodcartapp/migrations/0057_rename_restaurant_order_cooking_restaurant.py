# Generated by Django 3.2 on 2022-08-23 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0056_alter_orderelements_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='restaurant',
            new_name='cooking_restaurant',
        ),
    ]
