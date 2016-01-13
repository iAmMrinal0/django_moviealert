from django.shortcuts import render
from django.utils.timezone import now
from django.shortcuts import redirect
from moviealert.forms import MovieForm
import datetime


def home(request):
    today = datetime.date.today()
    movie_form = MovieForm()
    return render(request, "moviealert/index.html",
                  {"today": today, "now": now(), "form": movie_form})


def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")


def form_data(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            details = form.cleaned_data
            return render(request, "data.html", {"data": details})
        else:
            return redirect('/')
