# Generated by Django 5.0.6 on 2024-07-23 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_poll'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='created_by',
        ),
    ]
