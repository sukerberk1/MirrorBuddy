from django.shortcuts import render
from django.http import JsonResponse
from spotted.models import Entry

# Create your views here.

def jsondata(request):
    data = list(Entry.objects.values())
    return JsonResponse(data,safe = False)