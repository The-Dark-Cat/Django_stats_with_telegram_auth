import datetime

from django.shortcuts import render, redirect
from KeitaroStats.forms import KeitaroDateForm

# Create your views here.
from django.views import View

from KeitaroStats.keitaro_data import get_report


def index(request):
    return redirect('keitaro_stats')


class KeitaroStatsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('custom_user_login')
        context = {}
        date_form = KeitaroDateForm()
        context['date_form'] = date_form
        date_from = date_to = datetime.date.today()

        report = get_report(date_from, date_to, request.user.username)
        context['report'] = report

        return render(request, 'KeitaroStats/stats.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('custom_user_login')
        context = {}
        date_form = KeitaroDateForm(request.POST)
        context['date_form'] = date_form
        if date_form.is_valid():
            date_from = date_form.cleaned_data['date_from']
            date_to = date_form.cleaned_data['date_to']

            report = get_report(date_from, date_to)
            context['report'] = report

        return render(request, 'KeitaroStats/stats.html', context)