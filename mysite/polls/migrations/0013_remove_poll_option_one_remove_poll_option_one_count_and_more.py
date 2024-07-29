# Generated by Django 5.0.6 on 2024-07-29 12:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_poll_pub_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='option_one',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='option_one_count',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='option_three',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='option_three_count',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='option_two',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='option_two_count',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='question',
        ),
        migrations.AddField(
            model_name='poll',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='poll',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.poll'),
        ),
    ]
