from django.shortcuts import render
from django.shortcuts import redirect
from moviealert.forms import MovieForm


def home(request):
    form = MovieForm()
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            email = request.user.email
            instance = form.save(commit=False)
            instance.username = email
            instance.save()
            return redirect("form_data")
    return render(request, "moviealert/index.html", {"form": form})


def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")


def form_data(request):
    return render(request, "data.html")
