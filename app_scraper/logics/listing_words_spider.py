"""
This is the logic block for the same scanner.
Through we are trying to use Scrapy for this purpose.
"""

import json
import os
import re
import time

import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

start_time = time.time()

json_file = os.getcwd() + "\\app_scraper\\logics\\url_data.json"

with open(json_file, encoding='utf8') as json_data:
    url_data_dict = json.load(json_data)

LINK = url_data_dict['url_list']
WEBPAGE_LINKS = LINK
# WEBPAGE_LINKS = ['https://www.314e.com/']
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


print("\n\n")
# print(LINK)
print("\n\n")
print(WORDS_GROUPED)
print(len(WORDS_GROUPED))
print(f"\nExecuted in {(time.time() - start_time):.2f} seconds.\n")
print("\n\n")
