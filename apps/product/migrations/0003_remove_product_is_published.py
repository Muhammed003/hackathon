# Generated by Django 3.2 on 2022-06-16 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_published',
        ),
    ]
