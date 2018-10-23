# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as logout_user
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from app.models import Card, Comment, AppUser

def logout(request):
  logout_user(request)
  return HttpResponseRedirect('/')

def index(request):
  # Group cards by day and show 3 at a time
  paginator = Paginator(Card.objects.dates('date', 'day').reverse(), 3)

  page = request.GET.get('page')
  try:
    days = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    days = paginator.page(1)
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    days = paginator.page(paginator.num_pages)

  cards = dict()
  for d in days:
    k = 'Today' if d == d.today() else d.strftime('%a - %b. %d, %Y')
    cards[k] = Card.objects.filter(date__date=d)

  context = {
    'paginator': days,
    'cards': cards,
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

def claim(request, card_id):
  card = get_object_or_404(Card, pk=card_id)
  # Claim card when no one is assigned
  if not card.assigned:
    card.assigned = request.user
    card.save()

  # Unclaim a card th user claimed before
  elif card.assigned == request.user:
    card.assigned = None
    card.save()

  # Claim a card that was already claimed by another
  else:
    # TODO: Show a dialog that asks if the user is sure they want to do this
    card.assigned = request.user
    card.save()
  return HttpResponseRedirect('/')