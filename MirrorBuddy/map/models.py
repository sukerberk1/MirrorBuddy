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
            ('Samorząd uczniowski','Samorząd uczniowski'),
            ('Pedagog','Pedagog'),
            ('Psycholog','Psycholog')
        ]

    additional_info = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=40, choices=POSITION_CHOICES, default='Nauczyciel')

    def __str__(self):
        return self.name