import json
import os
import time

from django.contrib import messages
from django.shortcuts import render

from .logics.run_spiders import execute_all_jobs

# Create your views here.

logics_dir = os.getcwd() + "\\app_scraper\\logics\\"


def fetch_json_content(file_name):

    json_input_file = logics_dir + f'{file_name}.json'

    with open(json_input_file, encoding='utf8') as json_data:
        json_content = json.load(json_data)

    return json_content


def main_func(request):
    '''This is our main view function'''

    start_time = time.time()

    if request.method == "POST":

        post_url = request.POST['url']
        post_depth = int(request.POST['depth'])

        output_file = logics_dir + "input_post_data.json"
        input_data_dict = {'root_url': post_url,
                           'depth_level': post_depth}

        with open(output_file, 'w') as json_file:
            json.dump(input_data_dict, json_file)

        if 'https://' not in post_url:
            messages.error(request, "Error")

        else:
            execute_all_jobs()

            main_output_data = fetch_json_content('data_frequency')
            level = fetch_json_content('input_post_data')['depth_level']

            no_of_urls = len(fetch_json_content('url_data')['url_list'])

            common_words = main_output_data['common_words']
            common_word_pairs = main_output_data['common_word_pairs']

            context = {
                'level': level,
                'no_of_urls': no_of_urls,
                'common_words': common_words,
                'common_word_pairs': common_word_pairs,
            }

            print(f"\n\nExecuted in {(time.time() - start_time):.2f} seconds.")

            return render(request, 'index.html', context)

    print('\n\n')
    print(request.POST)
    print(f"\nExecuted in {(time.time() - start_time):.2f} seconds.\n\n")

    return render(request, 'index.html')
