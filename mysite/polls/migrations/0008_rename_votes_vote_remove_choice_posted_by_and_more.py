# Generated by Django 5.0.6 on 2024-07-12 09:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_rename_vote_votes_remove_choice_voter_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Votes',
            new_name='Vote',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='posted_by',
        ),
        migrations.AddField(
            model_name='choice',
            name='voter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='votes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='choice',
            name='votes',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Voter',
        ),
    ]
