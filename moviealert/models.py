from django.db import models as m


class RegionData(m.Model):
    bms_city = m.CharField(max_length=50)
    bms_city_url = m.URLField()


class TaskList(m.Model):
    username = m.EmailField()
    city = m.ForeignKey(RegionData, on_delete=m.CASCADE)
    movie_name = m.CharField(max_length=20)
    movie_language = m.CharField(max_length=20)
    movie_date = m.DateField()
    movie_found = m.BooleanField(default=False)
    task_completed = m.BooleanField(default=False)
    notified = m.BooleanField(default=False)
