# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    avatar512 = models.CharField(max_length=500)

    def __str__(self):
        return self.username

class Partner(models.Model):
  name = models.CharField(max_length=200)
  description = models.CharField(max_length=1000)
  logo = models.CharField(max_length=500)

  def __str__(self):
      return "%s" % (self.name)

class Card(models.Model):
    author = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE, related_name='cards'
    )
    body = models.CharField(max_length=1000)
    date = models.DateTimeField('date created', default=timezone.now)
    related_partners = models.ManyToManyField('Partner', related_name='cards', blank=True)
    assigned = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE,
      null=True, blank=True
    )

    def __str__(self):
      return "%s (%s)" % (self.body, self.author.get_full_name())

    class Meta:
      ordering = ['date',]

class Comment(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
    )
    body = models.CharField(max_length=1000)
    date = models.DateTimeField('date created', default=timezone.now)

    def __str__(self):
      return "%s (%s)" % (self.body, self.author.get_full_name())

    class Meta:
      ordering = ['date',]