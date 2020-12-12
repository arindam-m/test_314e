import os
import time

start_time = time.time()


def exe_scrapy_job():

    command = 'scrapy crawl run_scanner'
    os.system(command)

    print("\n\n")
    print(f"\n\nExecuted in {(time.time() - start_time):.2f} seconds.\n")
    print("\n\n")


exe_scrapy_job()
