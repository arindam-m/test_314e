"""
This is the logic block for our spider to crawl through,
to collect all the webpage-links for a given depth.
"""

import json
import os

import boto3
import scrapy
from scrapy.crawler import CrawlerProcess

logics_dir = os.getcwd() + '\\app_scraper\\logics\\'

json_input_file = logics_dir + "input_post_data.json"

with open(json_input_file, encoding='utf8') as json_data:
    input_data_dict = json.load(json_data)

root_index = input_data_dict['root_url']
WEBPAGE_LINKS = [root_index]

ACCESS_KEY = os.environ.get('S3_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY')

s3_resource = boto3.resource('s3',
                             aws_access_key_id=ACCESS_KEY,
                             aws_secret_access_key=SECRET_ACCESS_KEY)


class ListingURLs(scrapy.Spider):

    name = 'listing_urls'

    global WEBPAGE_LINKS

    start_urls = [root_index]

    links_to_ignore = ['#', 'javascript:void(0);', root_index]

    custom_settings = {
        'DEPTH_LIMIT': input_data_dict['depth_level'],
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
                    and link.startswith(root_index)
                    and link not in WEBPAGE_LINKS):
                WEBPAGE_LINKS.append(link)


if input_data_dict['depth_level'] > 0:

    process = CrawlerProcess()
    process.crawl(ListingURLs)
    process.start()


output_file = logics_dir + "url_data.json"
url_data_dict = {'url_list': WEBPAGE_LINKS}

with open(output_file, 'w') as json_file:
    json.dump(url_data_dict, json_file)
