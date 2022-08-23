# Generated by Django 3.2 on 2022-08-14 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0054_alter_order_payment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-status', 'registrated_at'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='orderelements',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_elements', to='foodcartapp.product', verbose_name='Продукт'),
        ),
    ]