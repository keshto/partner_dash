# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as logout_user

from app.models import Card, Comment, AppUser

def logout(request):
  logout_user(request)
  return HttpResponseRedirect('/')

def index(request):
  context = {
    'cards': Card.objects.all(),
  } if request.user.is_authenticated else {}

  return render(request, 'app/index.html', context)

def share(request):
  data = request.POST['data']
  if data:
    card = Card(author=request.user, body=data)
    card.save()
  return HttpResponseRedirect('/')

def reply(request, card_id):
  card = get_object_or_404(Card, pk=card_id)
  data = request.POST.get('data')
  if data:
    comment = card.comments.create(author=request.user, body=data)
    comment.save()
  return HttpResponseRedirect('/')