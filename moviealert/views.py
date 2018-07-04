from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from moviealert.forms import MovieForm
from moviealert.models import TaskList, RegionData
from datetime import date
import json


def home(request):
    form = MovieForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = MovieForm(request.POST)
        if form.is_valid():
            email = request.user.email
            instance = form.save(commit=False)
            instance.username = email
            instance.city = form.cleaned_data["city"]
            instance.save()
            return redirect("tasklist")
    return render(request, "moviealert/index.html", {"form": form})


def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")


def task_list(request):
    if request.user.is_authenticated:
        res = TaskList.objects.filter(username=request.user.email).values()
        today = date.today()
        return render(request, "moviealert/task_list.html",
                      {"data": res, "today": today})
    return redirect("/")


def get_city(request):
    if request.is_ajax():
        q = request.GET.get("term", "")
        regions = RegionData.objects.filter(bms_city__icontains=q)
        results = []
        for reg in regions:
            reg_json = {}
            reg_json["id"] = reg.id
            reg_json["label"] = reg.bms_city
            reg_json["value"] = reg.bms_city
            results.append(reg_json)
        data = json.dumps(results)
    else:
        data = "fail"
    mimetype = "application/json"
    return HttpResponse(data, mimetype)
