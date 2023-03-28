from django.shortcuts import render
from django.http import JsonResponse
from spotted.models import Entry
from misc.get_data import gather_news, gather_schedule, validate_schedule
# Create your views here.


def spotted_api(request):
    data = list(Entry.objects.values())
    return JsonResponse(data,safe = False)


def news_api(request, page):
    news = gather_news(page)
    return JsonResponse(news, safe=False)


def schedule_api(request, slug):
    grade, schedule_raw = gather_schedule(slug)
    schedule = validate_schedule(schedule_raw)
    return JsonResponse(schedule, safe=False)