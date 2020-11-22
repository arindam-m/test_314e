from django.http import JsonResponse
from django.shortcuts import render

from .scrape_logic import frequecy_data

# Create your views here.

url = "https://www.314e.com/"
level = 4


def main_func(request):

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

    return render(request, 'index.html', context)
