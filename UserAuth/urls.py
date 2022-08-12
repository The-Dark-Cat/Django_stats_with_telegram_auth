from django.urls import path

from UserAuth.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='custom_user_login'),
    path('login/<str:token>/', LoginView.as_view(), name='custom_user_login'),
]
