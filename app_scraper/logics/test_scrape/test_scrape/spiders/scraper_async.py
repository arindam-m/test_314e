"""
This is the logic block for the same scanner.

Through we are trying to use Scrapy for this purpose.
"""

import re
import string
import time
from collections import Counter, deque

import requests
import scrapy
from bs4 import BeautifulSoup

start_time = time.time()

root_index = "https://www.314e.com/"
_level = 2

URL_TRAVERSE_COUNT = 0


def url_crawler(url, level):
    '''...'''

    global URL_TRAVERSE_COUNT

    unique_urls = deque([url])
    considilated_urls_list = []

    traverse_index = level - 1

    while len(unique_urls) > 0:

        if traverse_index == 0:
            for _ in range(len(unique_urls)):
                url = unique_urls.popleft()
                considilated_urls_list.append(url)
            break

        for _ in range(len(unique_urls)):

            url = unique_urls.popleft()
            considilated_urls_list.append(url)

            response_obj = requests.get(url)
            soup = BeautifulSoup(response_obj.content, 'lxml')

            links_to_ignore = ['#', 'javascript:void(0);', url]
            anchors = soup.find_all('a')

            for anchor in anchors:
                link = anchor['href']
                if (link not in links_to_ignore
                        and link.startswith(url)
                        and link not in unique_urls):
                    unique_urls.append(link)

        traverse_index -= 1

    URL_TRAVERSE_COUNT = len(considilated_urls_list)

    return considilated_urls_list


# -----------------------------------------------------------------------------#


class ScanSpider(scrapy.Spider):
    '''Our very own Spider class'''

    name = "run_scanner"

    start_urls = [root_index]
    # start_urls = url_crawler(root_index, _level)

    def parse(self, response):

        # page = response.url.split(root_index)[-1][:-1].replace('/', '-')
        # if page == '':
        #     filename = "home.html"
        # else:
        #     filename = f"{page}.html"

        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        unique_urls = [root_index]
        links_to_ignore = ['#', 'javascript:void(0);', root_index]

        for link in response.css('a::attr(href)').getall():
            if (link not in links_to_ignore
                    and link.startswith(root_index)
                    and link not in unique_urls):
                unique_urls.append(link)

        print("\n\n")
        print(unique_urls)
        print(len(unique_urls))
        print(f"\n\nExecuted in {(time.time() - start_time):.2f} seconds.\n")
        print("\n\n")


# -----------------------------------------------------------------------------#


def words_gouped(url, level):
    '''...'''

    groups_of_words_list = []

    considilated_urls_list = url_crawler(url, level)

    for single_url in considilated_urls_list:

        response_obj = requests.get(single_url)
        response_obj.encoding = 'utf-8'
        soup = BeautifulSoup(response_obj.content, 'lxml')

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


# -----------------------------------------------------------------------------#


def frequecy_data(url, level):
    '''...'''

    groups_of_words_list = words_gouped(url, level)
    single_str = ' '.join(groups_of_words_list)
    single_words = re.findall(r"([\w+']+)", single_str.lower())

    word_pair_l = []

    for group_of_words in groups_of_words_list:
        words_with_punctuation = group_of_words.lower().split()

        list_of_punctuations = list(string.punctuation)

        for i in range(len(words_with_punctuation) - 1):
            if words_with_punctuation[i][-1] not in list_of_punctuations:
                next_word = words_with_punctuation[i + 1]
                if next_word[-1] in list_of_punctuations:
                    word_pair_l.append(
                        (words_with_punctuation[i], next_word[:-1]))
                else:
                    word_pair_l.append((words_with_punctuation[i], next_word))

    return_dict_object = {
        'no_of_urls': URL_TRAVERSE_COUNT,
        'common_words': [],
        'common_word_pairs': []
    }

    for i in range(10):

        single_word_tuple = Counter(single_words).most_common()[i]
        word = single_word_tuple[0]
        freq = single_word_tuple[1]
        if word in ('ehr', 'cdr', 'fhir'):
            word = word.upper()
        return_dict_object['common_words'].append({word: freq})

        word_pair_tuple = Counter(word_pair_l).most_common()[i]
        word_pair = word_pair_tuple[0][0] + ' ' + word_pair_tuple[0][1]
        freq = word_pair_tuple[1]
        return_dict_object['common_word_pairs'].append({word_pair: freq})

    return return_dict_object


# -----------------------------------------------------------------------------#
