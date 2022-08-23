# Generated by Django 3.2 on 2022-08-23 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0055_auto_20220814_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderelements',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='foodcartapp.order', verbose_name='Заказ'),
        ),
    ]