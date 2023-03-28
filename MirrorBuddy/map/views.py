from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Teacher
from misc.get_data import gather_schedule, get_headings_fast, validate_schedule, reformat_schedule, gather_news

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
        data = gather_schedule(slug)
    else:
        data = []
    # schedule var is a list consisting of title and a plan
    heading = data[0]
    schedule = validate_schedule(data[1]) # removes nan values and leaves strings only
    schedule = reformat_schedule(schedule) # reformats ([row],[row]..) to ([column], [column]..)
    return render(request, 'schedule_specific.html', {'schedule': schedule, 'heading': heading })

def news_view(request, pid):
    data = gather_news(pid)
    news_range = [x+1 for x in range(6)]
    return render(request, 'news.html', {'data': data, 'news_range': news_range, 'current': pid})
