"""
This is the logic block for the same scanner.
Through we are trying to use Scrapy for this purpose.
"""

import re
import time

import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

start_time = time.time()

WEBPAGE_LINKS = []
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


class UrlSpider(scrapy.Spider):

    name = 'url_spider'

    global WEBPAGE_LINKS

    root_index = 'https://www.314e.com/'
    start_urls = [root_index]

    WEBPAGE_LINKS = [root_index]
    links_to_ignore = ['#', 'javascript:void(0);', root_index]

    custom_settings = {
        'DEPTH_LIMIT': 1,
        # 'FEED_URI': 'data.json',
    }

    def parse(self, response):

        # print(f"\nExisting settings: {self.settings.attributes.keys()}")

        for next_page in WEBPAGE_LINKS:
            # yield scrapy.Request(next_page, callback=self.parse)
            yield response.follow(next_page, callback=self.parse)

        # json_file = os.getcwd() + "\\data.json"
        # raw = open(json_file, 'r+')
        # raw.truncate()

        # yield {
        #     'url_list': WEBPAGE_LINKS,
        # }

        for link in response.css('a::attr(href)').getall():
            if (link not in self.links_to_ignore
                    and link.startswith(self.root_index)
                    and link not in WEBPAGE_LINKS):
                WEBPAGE_LINKS.append(link)


class WordsSpider(scrapy.Spider):

    name = 'words_spider'
    start_urls = WEBPAGE_LINKS

    def parse(self, response):

        items = words_gouped(response)
        for item in items:
            WORDS_GROUPED.append((item))


def crawl_spiders(class_name):

    process = CrawlerProcess()
    process.crawl(class_name)
    process.start()


# crawl_spiders(UrlSpider)
crawl_spiders(WordsSpider)


print("\n\n")
print("\n\n")
print(WEBPAGE_LINKS)
print(len(WEBPAGE_LINKS))
print("\n\n")
print(WORDS_GROUPED)
print(len(WORDS_GROUPED))
print(f"\nExecuted in {(time.time() - start_time):.2f} seconds.\n")
print("\n\n")
