import time

# from django.http import JsonResponse
from django.shortcuts import render

from .logics.scraper_basic import frequecy_data

# Create your views here.

url = "https://www.314e.com/"
level = 1


def main_func(request):

    start_time = time.time()

    global url

    if request.method == "POST":
        url = request.POST['url']

    json_data = frequecy_data(url, level)

    # return JsonResponse(json_data)

    no_of_urls = json_data['no_of_urls']
    common_words = json_data['common_words']
    common_word_pairs = json_data['common_word_pairs']

    context = {
        'level': level,
        'no_of_urls': no_of_urls,
        'common_words': common_words,
        'common_word_pairs': common_word_pairs,
    }

    print(f"\n\nExecuted in {(time.time() - start_time):.2f} seconds.\n")

    return render(request, 'index.html', context)
