# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as logout_user
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from app.models import Partner, Card, Comment, AppUser, PartnerForm

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

  cards = list()
  for d in days:
    k = 'Today' if d == d.today() else d.strftime('%a - %b. %d, %Y')
    cards.append((k,Card.objects.filter(date__date=d).order_by('-date').prefetch_related('comments', 'author', 'assigned', 'related_partners')))

  context = {
    'paginator': days,
    'cards': cards if cards else [('Today', None)],
    'partners': Partner.objects.all(),
  } if request.user.is_authenticated else {}

  return render(request, 'app/index.html', context)

def partners(request):
  if request.method == 'POST':
    partner_id = request.POST.get('partnerID')
    
    if partner_id:
      partner = get_object_or_404(Partner, pk=partner_id)
      form = PartnerForm(request.POST, instance=partner)
    else:
      form = PartnerForm(request.POST)
      partner = None
    
    if form.is_valid():
      partner = Partner(**form.cleaned_data)
      partner.save()
      return HttpResponseRedirect('/partners/?partner=%s' % partner_id if partner_id else '/partners/')

  # if a GET (or any other method) we'll create a blank form
  else:
    form = PartnerForm(auto_id=True)
    partner = get_object_or_404(Partner, pk=request.GET.get('partner')) if request.GET.get('partner') else None

  context = {
    'partner': partner,
    'form': form,
    'form_details': PartnerForm(instance=partner),
    'partners': Partner.objects.all(),
  } if request.user.is_authenticated else {}
  return render(request, 'app/partners.html', context)

def partner_delete(request, partner_id):
  partner = get_object_or_404(Partner, pk=partner_id)
  partner.delete()
  return HttpResponseRedirect('/partners/')

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
    author = get_object_or_404(AppUser, pk=request.user.pk)
    comment = card.comments.create(author=author, body=data)
    comment.save()
    card.save()
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

def attach_partner_to_card(request, partner_id, card_id):
  partner = get_object_or_404(Partner, pk=partner_id)
  card = get_object_or_404(Card, pk=card_id)
  
  # Use partner module so not to update the modified timestamp in cards
  partner.cards.add(card)
  partner.save()
  return HttpResponseRedirect('/')

def detach_partner_to_card(request, partner_id, card_id):
  partner = get_object_or_404(Partner, pk=partner_id)
  card = get_object_or_404(Card, pk=card_id)
  
  # Use partner module so not to update the modified timestamp in cards
  partner.cards.remove(card)
  partner.save()
  return HttpResponseRedirect('/')