# Generated by Django 3.2 on 2022-08-14 17:33

import banners.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Слаг')),
            ],
        ),
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(upload_to=banners.models.get_upload_path, verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='banner',
            name='slug',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='banners', to='banners.slug', verbose_name='Слаг'),
        ),
    ]