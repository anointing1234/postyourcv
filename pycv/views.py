from django.shortcuts import render
import requests
import logging
import json
import os
import time
from urllib.parse import urljoin
from requests.exceptions import RequestException
from django.contrib.auth import logout
from bs4 import BeautifulSoup
import random
from accounts.models import POSITION_CHOICES, FOOT_CHOICES,VerifiedPlayer
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django_countries.fields import Country
from django_countries import countries
from datetime import date






def home_view(request):
    return render(request,'home/index.html')

def contact_view(request):
    player_name = request.GET.get('player_name', '')
    player_country = request.GET.get('player_country', '')

    context = {
        'player_name': player_name,
        'player_country': player_country,
    }
    return render(request,'home/contact.html',context)

def players_data(request):
    verified_players = VerifiedPlayer.objects.filter(is_verified=True)
    today = date.today()
    players_with_age = []
    for vp in verified_players:
        dob = vp.account.date_of_birth
        if dob:
            had_birthday = (today.month, today.day) >= (dob.month, dob.day)
            age = today.year - dob.year - (0 if had_birthday else 1)
        else:
            age = None
        players_with_age.append({
            'player': vp,
            'age': age
        })
    return render(request,'home/player_data.html', {
        'verified_players': verified_players,
         'players_with_age': players_with_age,
        # any other context you already have…
    })

def events_view(request):
    return render(request,'home/events.html')   

    
def player_view(request):
    user = request.user
    incomplete_fields = [
        not user.phone_number,
        not user.date_of_birth,
        not user.birth_place,
        not user.nationality,
        not user.height,
        not user.weight,
        not user.position,
        not user.preferred_foot,
    ]
    is_profile_incomplete = any(incomplete_fields)

    country_list = [(code, name) for code, name in countries]
    country_name = countries.name(request.user.nationality)  # Create a list of (code, name) tuples
    context = {
        'is_profile_incomplete': is_profile_incomplete,
        'country_name': country_name,
        'countries': country_list,
        'POSITION_CHOICES': POSITION_CHOICES,
        'FOOT_CHOICES': FOOT_CHOICES,
    }
    return render(request, 'home/Account.html',context)    




def send_message_view(request):
    return render(request,'auth/send_pass.html')