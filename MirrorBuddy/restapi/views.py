from django.shortcuts import render
from django.http import JsonResponse
from spotted.models import Entry
from misc.get_data import gather_schedule, validate_schedule, gather_list
import requests
from bs4 import BeautifulSoup

# Create your views here.

def spotted_data(request):
    data = list(Entry.objects.values())
    return JsonResponse(data,safe = False)


def schedule_data(request, slug):
    if len(slug)<5:
        data = gather_schedule(slug)
    else:
        data = []
    # schedule var is a list consisting of title and a plan
    schedule = validate_schedule(data[1]) # removes nan values and leaves strings only
    # schedule = reformat_schedule(schedule) # reformats ([row],[row]..) to ([column], [column]..)
    return JsonResponse(schedule, safe=False)


def news_data(request, page):
    news = gather_list(page)
    return JsonResponse(news, safe=False)