# Generated by Django 4.0.6 on 2022-12-02 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='position',
            field=models.CharField(choices=[('Dyrektor', 'Dyrektor'), ('Wicedyrektor', 'Wicedyrektor'), ('Nauczyciel', 'Nauczyciel'), ('Nauczyciel przedmiotów zawodowych', 'Nauczyciel przedmiotów zawodowych'), ('Samorząd uczniowski', 'Samorząd uczniowski')], default='Nauczyciel', max_length=40),
        ),
    ]