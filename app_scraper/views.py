import json
import os
import time

# from django.http import JsonResponse
from django.shortcuts import render

from .logics.run_spiders import execute_all_jobs
from .logics.scraper_basic import frequecy_data

# Create your views here.

url = "https://www.314e.com/"
# level = 1

logics_dir = os.getcwd() + "\\app_scraper\\logics\\"


def fetch_json_content(file_name):

    json_file = logics_dir + f'{file_name}.json'

    with open(json_file, encoding='utf8') as json_data:
        json_content = json.load(json_data)

    return json_content


level = fetch_json_content('depth_level')[0]


def main_func(request):

    start_time = time.time()

    global url

    if request.method == "POST":
        url = request.POST['url']

    execute_all_jobs()

    json_data = fetch_json_content('data_frequency')

    # json_data = frequecy_data(url, level)
    # return JsonResponse(json_data)
    # no_of_urls = json_data['no_of_urls']

    no_of_urls = len(fetch_json_content('url_data')['url_list'])

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
