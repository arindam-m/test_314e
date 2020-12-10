from django.test import TestCase

from .logics import scraper_basic as sb

# Create your tests here.


class TestScrapeLogic(TestCase):

    def setUp(self):
        self.url = "https://www.314e.com/"
        self.level = 1

    def test_url_crawler(self):
        result = sb.url_crawler(self.url, self.level)
        self.assertEqual(len(result), 1)
