# Generated by Django 5.0.6 on 2024-08-02 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0022_alter_choice_choice_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(max_length=255),
        ),
    ]
