from typing import Any
from django.db import models
from django.utils import timezone
from django.contrib import admin
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    poll = models.ForeignKey('Poll', on_delete=models.SET_NULL, null=True, blank=True)
    pub_date = models.DateTimeField("date published",default=timezone.now )
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    voter = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="votes", null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.choice_text
    
# class Voter(models.Model):
#     user = models.ForeignKey( User)
#     poll = models.ForeignKey(Question)


def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Vote(models.Model):
    choice = models.ForeignKey(Choice,on_delete=models.CASCADE)
    voter = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        if self.voter.get_full_name():
            return self.voter.get_full_name()
        else:
            return self.voter.username
        
class Poll(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    pub_date = models.DateTimeField("date published",default=timezone.now)

    def __str__(self):
        return self.name if self.name else 'Null'
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now