from django.shortcuts import render
from .models import *
import datetime
# Create your views here.

def spotted_view(request):
    submitted = False
    if request.method=="POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            e = Entry()
            e.text = form.cleaned_data['text']
            if e.nickname!='':
                e.nickname = form.cleaned_data['nickname']
            else:
                e.nickname = 'Anonim'
            e.pub_date = datetime.datetime.now()
            e.save()
            submitted = True

    form = EntryForm()
    entry_list = Entry.objects.all().order_by('-pub_date')[:15]
    return render(request,'spottedapp.html',{'form': form, 'entry_list': entry_list, 'submitted': submitted})