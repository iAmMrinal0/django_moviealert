from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import TaskList, RegionData
from .api import kimono
from datetime import datetime
import requests


def validate(db_value, response_value):
    if db_value.lower() in response_value.lower():
        return True
    else:
        return False


def find_show_url(row, city_url):
    url = "{0}{1}".format(kimono.KIMONO_URL, kimono.MOVIE_LIST_ID)
    kimpath1 = city_url.rsplit("/", 2)[1]
    data = {"apikey": kimono.APIKEY, "kimpath1": kimpath1}
    response = requests.get(url, params=data)
    movies = response.json()
    for val in movies["results"]["bms_city_movies"]:
        if (validate(row["movie_name"], val["bms_movie_name"]) and
                validate(row["movie_language"], val["bms_movie_language"])):
            return val["bms_movie_book"]


def find_movie_times(row, show_url):
    url = "{0}{1}".format(kimono.KIMONO_URL, kimono.MOVIE_TIME_ID)
    url_split = show_url.rsplit("/", 5)
    kimpath2 = url_split[2]
    kimpath3 = url_split[3]
    str_date = str(row["movie_date"])
    bms_date_format = datetime.strptime(
        str_date, "%Y-%m-%d").strftime("%Y%m%d")
    kimpath4 = bms_date_format
    data = {"apikey": kimono.APIKEY, "kimpath2": kimpath2,
            "kimpath3": kimpath3, "kimpath4": kimpath4, "kimmodify": 1}
    response = requests.get(url, params=data)
    times = response.json()
    return times


def verify_times(row, data):
    db_date = str(row["movie_date"])[8:10]
    strp_date = data["results"]["bms_movie"][0]["bms_movie_date"]
    if db_date != strp_date:
        return False
    return True


def search_movie():
    result = TaskList.objects.filter(task_completed=False,
                                     movie_date__gte=datetime.now()).values()
    for row in result:
        city_url = RegionData.objects.get(id=row["city_id"]).bms_city_url
        show_url = find_show_url(row, city_url)
        if show_url:
            movie_times = find_movie_times(row, show_url)
            ctx = {"data": movie_times}
            if verify_times(row, movie_times):
                mail_content = render_to_string("email.html", ctx).strip()
                send_mail("Movie Alert found your movie!", "",
                          settings.EMAIL_HOST_USER, [row["username"]],
                          fail_silently=False, html_message=mail_content)
                upd_db = TaskList.objects.get(pk=row["id"])
                upd_db.task_completed = True
                upd_db.notified = True
                upd_db.movie_found = True
                upd_db.save()
