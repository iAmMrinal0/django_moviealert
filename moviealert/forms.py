from django import forms
from django.conf import settings
from moviealert.base.widgets import CalendarWidget
from .models import TaskList, RegionData


class MovieForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        self.fields['movie_date'] = forms.DateField(
            widget=CalendarWidget(attrs={"readonly": "readonly",
                                         "style": "background:white;"}),
            input_formats=settings.ALLOWED_DATE_FORMAT)
        self.fields["city"] = forms.CharField(
            widget=forms.TextInput(attrs={"id": "txtSearch"}))
        self.fields["city"].label = "City Name"

    def clean(self):
        cleaned_data = super(MovieForm, self).clean()
        cleaned_data['city'] = RegionData.objects.get(
            bms_city=cleaned_data['city'])

    class Meta:
        model = TaskList
        exclude = ("username", "task_completed", "notified", "movie_found",)
