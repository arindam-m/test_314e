from django.http import JsonResponse
from django.shortcuts import render

from .scrape_logic import frequecy_data

# Create your views here.

url = "https://www.314e.com/"
level = 1

def main_func(request):

    return_data = frequecy_data(url, level)

    # return JsonResponse(return_data)
    return render(request, 'index.html')
