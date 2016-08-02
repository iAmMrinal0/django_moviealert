from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import TaskList, RegionData
from datetime import datetime
import requests


ROOT_URL = "https://in.bookmyshow.com"


def validate(db_value, response_value):
    if db_value.lower() in response_value.lower():
        return True
    else:
        return False


def find_show_url(row, city_url):
    url = city_url
    headers = {
        "User-Agent":
        ("Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) "
         "Gecko/20100101 Firefox/36.0")
    }
    response = requests.get(url, headers=headers)
    source = BeautifulSoup(response.content, "html.parser")
    tags = source.find_all("section",
                           attrs={"class": "language-based-formats"})
    for tag in tags:
        c = tag.find_all("a")
        h = tag.find_all("h2")
        m_name = row["movie_name"].lower().replace(" ", "-")
        if (validate(row["movie_language"].lower(), h[0].text.lower()) and
                validate(m_name, c[0]["href"])):
            return c[0]["href"]


def find_movie_times(row, show_url):
    headers = {
        "User-Agent":
        ("Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) "
         "Gecko/20100101 Firefox/36.0")
    }
    bms_date_format = row["movie_date"].strftime("%Y%m%d")
    show_url = show_url[:-9]
    url = "{0}{1}{2}".format(ROOT_URL, show_url, bms_date_format)
    response = requests.get(url, headers=headers)
    source = BeautifulSoup(response.content, "html.parser")
    m_name = source.find("h1", attrs={"itemprop": "name"})
    date_scrap = source.find("li", attrs={"class": "_active"})
    if m_name:
        fn = {}
        fn["results"] = {}
        fn["results"]["bms_movie"] = []
        fn["results"]["bms_movie"].append(
            {"bms_movie_name": m_name["content"]})
        date_scraped = date_scrap.div.text
        fn["results"]["bms_movie"][-1]["bms_movie_date"] = date_scraped[:2]
        fn["results"]["bms_timings"] = []
        cinema_halls = source.find_all("div", attrs={"class": "container"})
        for cinema in cinema_halls:
            halls = cinema.find_all("li", attrs={"class": "list"})
            for temp in halls:
                if temp["data-is-down"] == "false":
                    times = temp.find_all("div", attrs={"data-online": "Y"})
                    if times:
                        fn["results"]["bms_timings"].append(
                            {"bms_movie_hall": temp["data-name"]})
                        fn["results"]["bms_timings"][-1]["bms_show_times"] = []
                        for time in times:
                            show_link = time.a["href"].strip()
                            fn["results"][
                                "bms_timings"][-1]["bms_show_times"].append(
                                    {"text": time.text.strip(),
                                     "href": "{0}{1}".format(ROOT_URL,
                                                             show_link)})
                    else:
                        return False
        return fn
    return False


def verify_times(row, data):
    db_date = str(row["movie_date"])[8:10]
    strp_date = data["results"]["bms_movie"][0]["bms_movie_date"]
    if db_date != strp_date:
        return False
    return True


def mail(row, context):
    mail_content = render_to_string("email.html", context).strip()
    return send_mail("Movie Alert found your movie!", "",
                     settings.EMAIL_HOST_USER, [row["username"]],
                     fail_silently=False, html_message=mail_content)


def update_db(row):
    upd_db = TaskList.objects.get(pk=row["id"])
    upd_db.task_completed = True
    upd_db.notified = True
    upd_db.movie_found = True
    upd_db.save()


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
                if mail(row, ctx):
                    update_db(row)
