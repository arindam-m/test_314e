from django.test import TestCase

from . import scrape_logic as sl

# Create your tests here.

class TestScrapeLogic(TestCase):

    def setUp(self):
        self.url = "https://www.314e.com/"
        self.level = 1

    def test_url_crawler(self):
        result = sl.url_crawler(self.url, self.level)
        self.assertEqual(len(result), 1)