from django.shortcuts import render
from django.utils.timezone import now
import datetime


def home(request):
    today = datetime.date.today()
    return render(request, "moviealert/index.html",
                  {"today": today, "now": now()})


def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")
