from django.db import models as m


class TaskList(m.Model):
    username = m.EmailField()
    city_name = m.CharField(max_length=20)
    movie_name = m.CharField(max_length=20)
    movie_language = m.CharField(max_length=20)
    movie_date = m.DateField()
