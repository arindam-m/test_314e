import os
import time

start_time = time.time()


def exe_run_spiders(file_name):

    cwd = os.getcwd() + '\\app_scraper\\logics\\'
    command = 'python ' + cwd + f'{file_name}.py'
    os.system(command)


def execute_all_jobs():

    spider_files = [
        'listing_urls_spider',
        'listing_words_spider',
    ]

    for file in spider_files:
        exe_run_spiders(file)

    print(f"\n\nExecuted in {(time.time() - start_time):.2f} seconds.\n")


execute_all_jobs()
