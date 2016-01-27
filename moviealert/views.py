from django.shortcuts import render
from django.shortcuts import redirect
from moviealert.forms import MovieForm
from moviealert.models import TaskList
from datetime import date


def home(request):
    form = MovieForm()
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            email = request.user.email
            instance = form.save(commit=False)
            instance.username = email
            instance.save()
            return redirect("tasklist")
    return render(request, "moviealert/index.html", {"form": form})


def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")


def task_list(request):
    if request.user.is_authenticated():
        res = TaskList.objects.filter(username=request.user.email).values()
        today = date.today()
        return render(request, "moviealert/task_list.html",
                      {"data": res, "today": today})
    return redirect("/")
