# Generated by Django 5.0.6 on 2024-07-04 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_memberform'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memberform',
            old_name='password1',
            new_name='confirm_password',
        ),
        migrations.RenameField(
            model_name='memberform',
            old_name='password2',
            new_name='password',
        ),
    ]
