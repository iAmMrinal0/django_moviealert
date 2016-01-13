from django import forms
from django.conf import settings
from moviealert.base.widgets import CalendarWidget
from .models import TaskList


class MovieForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        self.fields['movie_date'] = forms.DateField(
            widget=CalendarWidget,
            input_formats=settings.ALLOWED_DATE_FORMAT)

    class Meta:
        model = TaskList
        exclude = ("username",)
