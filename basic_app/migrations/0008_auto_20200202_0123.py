# Generated by Django 2.2.5 on 2020-02-01 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0007_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='requested_quantity',
        ),
    ]
