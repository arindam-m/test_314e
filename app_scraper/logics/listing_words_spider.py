"""
This is the logic block for our spider, to collect all the grouped words
from a list of urls scraped in the previous module.
"""

import json
import os
import re

import boto3
import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

ACCESS_KEY = os.environ.get('S3_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY')

s3_resource = boto3.resource('s3',
                             aws_access_key_id=ACCESS_KEY,
                             aws_secret_access_key=SECRET_ACCESS_KEY)

logics_dir = os.getcwd() + '\\app_scraper\\logics\\'

input_file = "url_data.json"

# with open(logics_dir + input_file, encoding='utf8') as json_data:
#     url_data_dict = json.load(json_data)

json_data = s3_resource.Object('test-314e',
                               f'jsons/{input_file}').get()['Body']

url_data_dict = json.loads(json_data.read().decode('utf-8'))

WEBPAGE_LINKS = url_data_dict['url_list']
WORDS_GROUPED = []


def words_gouped(response):
    '''...'''

    groups_of_words_list = []

    soup = BeautifulSoup(response.body, 'lxml')

    # Scraping from Span section

    for span_content in soup.find_all('span'):
        if (span_content.text != '') and (span_content.text != '\n'):
            groups_of_words_list.append(span_content.text)

    # Scraping from Main section

    words_in_paras_list_raw = []

    for main_content in soup.find_all('main'):
        if (main_content.text != '') and (main_content.text != '\n'):
            words_in_paras_list_raw.append(main_content.text)

    words_list_main = []

    for words_para in words_in_paras_list_raw:
        str_list = (re.split(r"[\n\t]", words_para))
        for single_str in str_list:
            if single_str not in ('', ' '):
                if single_str.endswith(' '):
                    words_list_main.append(single_str[:-1])
                elif single_str.endswith('...Read More'):
                    words_list_main.append(single_str[:-12])
                    words_list_main.append(single_str[-9:])
                else:
                    words_list_main.append(single_str)

    groups_of_words_list += words_list_main

    return groups_of_words_list


class WordsSegregator(scrapy.Spider):

    name = 'words_spider'
    start_urls = WEBPAGE_LINKS

    def parse(self, response):

        items = words_gouped(response)
        for item in items:
            WORDS_GROUPED.append((item))


process = CrawlerProcess()
process.crawl(WordsSegregator)
process.start()


output_file = "words_grouped_data.json"

# with open(logics_dir + output_file, 'w') as json_file:
#     json.dump(WORDS_GROUPED, json_file)

s3_resource.Object(
    'test-314e',
    f'jsons/{output_file}').put(Body=json.dumps(WORDS_GROUPED))
