# Generated by Django 3.2 on 2022-08-08 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0039_auto_20220808_1122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='last_name',
            new_name='lastname',
        ),
    ]
