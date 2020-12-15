"""
This is the logic block for the same scanner.
Through we are trying to use Scrapy for this purpose.
"""

import json
import os
# import time

import scrapy
from scrapy.crawler import CrawlerProcess

# start_time = time.time()

WEBPAGE_LINKS = []


class ListingURLs(scrapy.Spider):

    name = 'listing_urls'

    global WEBPAGE_LINKS

    root_index = 'https://www.314e.com/'
    start_urls = [root_index]

    WEBPAGE_LINKS = [root_index]
    links_to_ignore = ['#', 'javascript:void(0);', root_index]

    custom_settings = {
        'DEPTH_LIMIT': 4,
        # 'FEED_URI': 'data.json',
    }

    def parse(self, response):

        # print(f"\nExisting settings: {self.settings.attributes.keys()}")

        for next_page in WEBPAGE_LINKS:
            # yield scrapy.Request(next_page, callback=self.parse)
            yield response.follow(next_page, callback=self.parse)

        # output_file = os.getcwd() + "\\data.json"
        # raw = open(output_file, 'r+')
        # raw.truncate()

        # yield {
        #     'url_list': WEBPAGE_LINKS,
        # }

        for link in response.css('a::attr(href)').getall():
            if (link not in self.links_to_ignore
                    and link.startswith(self.root_index)
                    and link not in WEBPAGE_LINKS):
                WEBPAGE_LINKS.append(link)


process = CrawlerProcess()
process.crawl(ListingURLs)
process.start()


output_file = os.getcwd() + "\\app_scraper\\logics\\url_data.json"
url_data_dict = {'url_list': WEBPAGE_LINKS}

with open(output_file, 'w') as json_file:
    json.dump(url_data_dict, json_file)


# print("\n\n")
# print("\n\n")
# # print(WEBPAGE_LINKS)
# print(len(WEBPAGE_LINKS))
# print(f"\nExecuted in {(time.time() - start_time):.2f} seconds.\n")
# print("\n\n")
