import os
from random import randint

from django.contrib.auth import login
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from UserAuth.models import TempToken, User, UserWhitelist


class LoginView(View):
    def get(self, request, token=None):
        context = {}
        if request.user.is_authenticated:
            return redirect('keitaro_stats')
        else:
            # token = request.GET.get('token')
            if token:
                try:
                    temp_token = TempToken.objects.get(token=token)
                    if temp_token.is_active:
                        with transaction.atomic():
                            user = temp_token.user
                            temp_token.is_active = False
                            temp_token.save()
                            # authenticate user
                            login(request, user)
                        return redirect('keitaro_stats')
                    else:
                        context['exception'] = 'Token is not active'
                except TempToken.DoesNotExist:
                    context['exception'] = 'Token is not found'
            else:
                return redirect('http://t.me/djangocatbot')
        return render(request, 'UserAuth/login.html', context)

    def post(self, request):
        return render(request, 'UserAuth/login.html')
