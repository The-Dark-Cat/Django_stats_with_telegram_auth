import datetime

from django import forms


class KeitaroDateForm(forms.Form):
    date_from = forms.DateField(label='Date from', input_formats=['%Y-%m-%d'],
                                widget=forms.SelectDateWidget(
                                    years=range(datetime.datetime.now().year, datetime.datetime.now().year - 20, -1),
                                    attrs={'class': 'date-form'}),
                                initial=datetime.date.today(),
                                )
    date_to = forms.DateField(label='Date to', input_formats=['%Y-%m-%d'],
                              widget=forms.SelectDateWidget(
                                  years=range(datetime.datetime.now().year, 2000, -1),
                                  attrs={'class': 'date-form'}),
                              initial=datetime.date.today())
    # name = forms.CharField(label='Name', max_length=100)

    def is_valid(self):
        if super().is_valid():
            if self.cleaned_data['date_from'] > self.cleaned_data['date_to']:
                self.add_error('date_from', 'Date from must be less than date to')
                return False
            return True


