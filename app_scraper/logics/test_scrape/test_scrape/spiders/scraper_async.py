"""
This is the logic block for the same scanner.
Through we are trying to use Scrapy for this purpose.
"""

import time

import scrapy

start_time = time.time()
root_index = "https://www.314e.com/"
WEB_PAGE_LINKS = [root_index]


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
            yield scrapy.Request(next_page, callback=self.parse)

        print("\n\n")
        print(len(WEB_PAGE_LINKS))
        # print(f"\n\nExecuted in {(time.time() - start_time):.2f} seconds.\n")
        print("\n\n")

        links_to_ignore = ['#', 'javascript:void(0);', root_index]

        for link in response.css('a::attr(href)').getall():
            if (link not in links_to_ignore
                    and link.startswith(root_index)
                    and link not in WEB_PAGE_LINKS):
                WEB_PAGE_LINKS.append(link)
