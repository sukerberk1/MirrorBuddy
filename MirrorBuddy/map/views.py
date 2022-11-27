from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.


class Home(TemplateView):
    template_name = "base.html"


def map_finder(request):
    form = 1
    return render(request, 'map_finder.html', {'form': form})