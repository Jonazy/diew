from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import Preference
from django.contrib import messages
# Create your views here.


def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    exists = Preference.objects.filter(user=request.user).exists()
    user_preference = None
    if exists:
        user_preference = Preference.objects.filter(user=request.user)
    if request.method == "GET":
        return render(request, 'preferences/index.html',
                      {"currencies": currency_data, "user_preference": user_preference})
    if request.method == "POST":
        currency = request.POST.get('user_option')
        if exists:
            user_preference.currency = currency
            user_preference.update()
        else:
            user_preference = Preference.objects.create(user=request.user, currency=currency)
        messages.success(request, "Changes saved successfully")
    return render(request, 'preferences/index.html', {"currencies": currency_data, "user_preference": user_preference})