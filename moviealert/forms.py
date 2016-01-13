from django import forms
from django.conf import settings
from moviealert.base.widgets import CalendarWidget


class MovieForm(forms.Form):

    city_name = forms.CharField(label="City Name", max_length=20)
    movie_name = forms.CharField(label="Movie Name", max_length=25)
    language = forms.CharField(label="Language", max_length=20)
    movie_date = forms.DateField(
        widget=CalendarWidget, input_formats=settings.ALLOWED_DATE_FORMAT)
