# Generated by Django 3.2 on 2022-08-11 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0052_auto_20220811_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='foodcartapp.restaurant', verbose_name='Готовящий ресторан'),
        ),
    ]
