from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Teacher

# Create your views here.


class Home(TemplateView):
    template_name = "base.html"


def map_finder(request):
    data = []
    if 'search' in request.GET:
        search_term = request.GET.get("search")
        data = Teacher.objects.all().filter(name__icontains=search_term) | Teacher.objects.all().filter(position__icontains=search_term) | Teacher.objects.all().filter(additional_info__icontains=search_term) 
    return render(request, 'map_finder.html', {'data': data})


class MirrorSelfie(TemplateView):
    template_name = "mirror_selfie.html" 