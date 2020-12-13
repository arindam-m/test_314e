"""
This is the logic block for the same scanner.
Through we are trying to use Scrapy for this purpose.
"""

import re
import time

import scrapy
from bs4 import BeautifulSoup

start_time = time.time()
root_index = "https://www.314e.com/"
WEB_PAGE_LINKS = [root_index]


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


class ScanSpider(scrapy.Spider):
    '''Our very own Spider class'''

    global WEB_PAGE_LINKS

    name = "run_scanner"

    start_urls = WEB_PAGE_LINKS

    custom_settings = {
        'DEPTH_LIMIT': 4,
    }

    def parse(self, response):

        # print(f"\n\n{response.status}\n")

        for next_page in WEB_PAGE_LINKS:
            # yield scrapy.Request(next_page, callback=self.parse)
            yield response.follow(next_page, callback=self.parse)

        links_to_ignore = ['#', 'javascript:void(0);', root_index]

        for link in response.css('a::attr(href)').getall():
            if (link not in links_to_ignore
                    and link.startswith(root_index)
                    and link not in WEB_PAGE_LINKS):
                WEB_PAGE_LINKS.append(link)

        print("\n\n")
        print(len(WEB_PAGE_LINKS))
        print(f"\nExecuted in {(time.time() - start_time):.2f} seconds.\n")
        print("\n\n")

        # yield {
        #     'url_list': WEB_PAGE_LINKS
        # }
