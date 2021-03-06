# Generated by Django 2.2.5 on 2020-02-02 14:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0009_remove_custprofileinfo_has_ordered_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custprofileinfo',
            name='Address',
            field=models.CharField(default=None, max_length=240),
        ),
        migrations.AlterField(
            model_name='custprofileinfo',
            name='Name',
            field=models.CharField(default=None, max_length=240),
        ),
        migrations.AlterField(
            model_name='custprofileinfo',
            name='Phone',
            field=models.IntegerField(default=None, unique=True, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)]),
        ),
        migrations.AlterField(
            model_name='custprofileinfo',
            name='Zipcode',
            field=models.IntegerField(default=None, validators=[django.core.validators.MinValueValidator(100000), django.core.validators.MaxValueValidator(999999)]),
        ),
        migrations.AlterField(
            model_name='vendorprofileinfo',
            name='Address',
            field=models.CharField(default=None, max_length=240),
        ),
        migrations.AlterField(
            model_name='vendorprofileinfo',
            name='Name',
            field=models.CharField(default=None, max_length=240),
        ),
        migrations.AlterField(
            model_name='vendorprofileinfo',
            name='Phone',
            field=models.IntegerField(default=None, unique=True, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)]),
        ),
        migrations.AlterField(
            model_name='vendorprofileinfo',
            name='Shop_Name',
            field=models.CharField(default=None, max_length=240),
        ),
    ]
