from django.db import models
from django import forms

# Create your models here.

class Entry(models.Model):
    nickname = models.TextField(max_length=100, null=True, blank=True)
    text = models.TextField(max_length=1500)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.text+' --- Entry no'+str(self.id)


class EntryForm(forms.Form):
    nickname = forms.CharField(max_length=100, required=False, label="Nick (niewymagane)")
    text = forms.CharField(label='Napisz coś:', max_length=1500, widget=forms.Textarea(attrs={'rows': 2}))