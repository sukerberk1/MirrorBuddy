from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Teacher
from misc.gather_data import gather_schedule, get_headings_fast

# Create your views here.


class Home(TemplateView):
    template_name = "base.html"


def map_finder(request):
    data = []
    if 'search' in request.GET:
        search_term = request.GET.get("search")
        data = Teacher.objects.all().filter(name__icontains=search_term) | Teacher.objects.all().filter(position__icontains=search_term) | Teacher.objects.all().filter(additional_info__icontains=search_term) 
    return render(request, 'map_finder.html', {'data': data})


def schedule_finder(request):
    data = get_headings_fast()
    if 'search' in request.GET:
        search_term = request.GET.get("search")
        data_temp = []
        for item in data:
            if search_term.replace(' ','').upper() in item[0].replace(' ','').upper():
                data_temp.append(item)
        data = data_temp
    return render(request, 'schedule_finder.html', {'data': data})

def schedule_specific(request, slug):
    if len(slug)<5:
        schedule = gather_schedule(slug)
    else:
        schedule = []
    return render(request, 'schedule_specific.html', {'schedule': schedule})