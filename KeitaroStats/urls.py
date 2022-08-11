from django.urls import path

from KeitaroStats.views import KeitaroStatsView

urlpatterns = [
    path('', KeitaroStatsView.as_view(), name='keitaro_stats'),
]