"""partner_dash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^partners/', views.partners, name='partners'),
    url(r'^delete/(?P<partner_id>.+)$', views.partner_delete, name='partner_delete'),
    url(r'^share/', views.share, name='share'),
    url(r'^reply/(?P<card_id>[0-9]+)$', views.reply, name='reply'),
    url(r'^claim/(?P<card_id>[0-9]+)$', views.claim, name='claim'),
    url(r'^attach_partner_to_card/(?P<partner_id>.+)/(?P<card_id>[0-9]+)$', views.attach_partner_to_card, name='attach_partner_to_card'),
    url(r'^detach_partner_to_card/(?P<partner_id>.+)/(?P<card_id>[0-9]+)$', views.detach_partner_to_card, name='detach_partner_to_card'),
    url('', include('social_django.urls', namespace='slack')),
    url(r'^logout/', views.logout, name='logout'),
]
