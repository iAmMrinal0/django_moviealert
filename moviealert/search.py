from django.core.mail import send_mail
from .models import TaskList
from .api import kimono
import datetime
import json
import requests


def load_regions():
    with open("moviealert/fixtures/regions.json") as f:
        region_data = json.loads(f.read())
    return region_data


def find_city_url(row, region_data):
    for val in region_data["results"]["bms_city"]:
        if row["city_name"].lower() in val["city"]["text"].lower():
            return val["city"]["href"]


def find_show_url(row, city_url):
    url = "{0}{1}".format(kimono.KIMONO_URL, kimono.MOVIE_LIST_ID)
    kimpath1 = city_url.rsplit("/", 2)[1]
    data = {"apikey": kimono.APIKEY, "kimpath1": kimpath1}
    response = requests.get(url, params=data)
    movies = response.json()
    for val in movies["results"]["bms_city_movies"]:
        if (row["movie_name"].lower() in val["bms_movie_name"].lower() and
                row["movie_language"].lower() in val["bms_movie_language"].lower()):
            return val["bms_movie_book"]


def find_movie_times(row, show_url):
    url = "{0}{1}".format(kimono.KIMONO_URL, kimono.MOVIE_TIME_ID)
    url_split = show_url.rsplit("/", 5)
    kimpath2 = url_split[2]
    kimpath3 = url_split[3]
    str_date = str(row["movie_date"])
    bms_date_format = datetime.datetime.strptime(
        str_date, "%Y-%m-%d").strftime("%Y%m%d")
    kimpath4 = bms_date_format
    data = {"apikey": kimono.APIKEY, "kimpath2": kimpath2,
            "kimpath3": kimpath3, "kimpath4": kimpath4}
    response = requests.get(url, params=data)
    times = response.json()
    return times


def search_movie():
    region_data = load_regions()
    result = TaskList.objects.filter(task_completed=False).values()
    for row in result:
        city_url = find_city_url(row, region_data)
        show_url = find_show_url(row, city_url)
        movie_times = find_movie_times(row, show_url)
        send_mail("Movie Alert found your movie!", row["movie_name"],
                  "moviealert.mailer@gmail.com",
                  [row["username"]], fail_silently=False)
