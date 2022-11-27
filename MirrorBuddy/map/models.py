from django.db import models

# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    classroom = models.IntegerField()

    POSITION_CHOICES = [
            ('Dyrektor', 'Dyrektor'),
            ('Wicedyrektor', 'Wicedyrektor'),
            ('Nauczyciel', 'Nauczyciel'),
            ('Nauczyciel przedmiotów zawodowych', 'Nauczyciel przedmiotów zawodowych'),
        ]

    position = models.CharField(max_length=40, choices=POSITION_CHOICES, default='Nauczyciel')
