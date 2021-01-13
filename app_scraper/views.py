import json
import os
from time import sleep
from platform import system

import boto3
from django.contrib import messages
# from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .logics.run_spiders import execute_all_jobs

ACCESS_KEY = os.environ.get('S3_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY')

s3_resource = boto3.resource('s3',
                             aws_access_key_id=ACCESS_KEY,
                             aws_secret_access_key=SECRET_ACCESS_KEY)

if system() == 'Linux':
    logics_dir = os.getcwd() + "/app_scraper/logics/"
elif system() == 'Windows':
    logics_dir = os.getcwd() + "\\app_scraper\\logics\\"


def fetch_json_content(file_name):

    input_file = f'{file_name}.json'

    # with open(logics_dir + input_file, encoding='utf8') as json_data:
    #     json_content = json.load(json_data)

    json_data = s3_resource.Object('test-314e',
                                   f'jsons/{input_file}').get()['Body']

    json_content = json.loads(json_data.read().decode('utf-8'))

    return json_content


def main_func(request):
    '''This is our main view function'''

    if request.method == "POST":

        post_url = request.POST['url']
        post_depth = int(request.POST['depth'])

        output_file = "input_post_data.json"
        input_data_dict = {'root_url': post_url,
                           'depth_level': post_depth}

        # with open(logics_dir + output_file, 'w') as json_file:
        #     json.dump(input_data_dict, json_file)

        # s3_resource.create_bucket(Bucket='my_bucket')

        s3_resource.Object(
            'test-314e',
            f'jsons/{output_file}').put(Body=json.dumps(input_data_dict))

        if 'https://' not in post_url:
            messages.error(request, "Error")

        else:

            output_file = "data_frequency.json"
            empty_dict = {}
            s3_resource.Object(
                'test-314e',
                f'jsons/{output_file}').put(Body=json.dumps(empty_dict))

            result = execute_all_jobs.apply_async()

            context = {
                'task_id': result.task_id,
            }

            return render(request, 'index.html', context)

    return render(request, 'index.html')


def func_present_data(request):

    main_output_data = fetch_json_content('data_frequency')

    while len(main_output_data) == 0:
        sleep(0.75)
        main_output_data = fetch_json_content('data_frequency')

    level = fetch_json_content('input_post_data')['depth_level']
    no_of_urls = len(fetch_json_content('url_data')['url_list'])

    single_words = main_output_data['single_words']
    common_words = main_output_data['common_words']
    common_word_pairs = main_output_data['common_word_pairs']

    context = {
        'level': level,
        'no_of_urls': no_of_urls,
        'single_words': single_words,
        'common_words': common_words,
        'common_word_pairs': common_word_pairs,
    }

    return render(request, 'data-table.html', context)
