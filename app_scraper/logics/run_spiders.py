import json
import os
import re
import string
# import time
from collections import Counter

import boto3

# start_time = time.time()

ACCESS_KEY = os.environ.get('S3_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY')

s3_resource = boto3.resource('s3',
                             aws_access_key_id=ACCESS_KEY,
                             aws_secret_access_key=SECRET_ACCESS_KEY)

logics_dir = os.getcwd() + '\\app_scraper\\logics\\'


def execute_all_jobs():

    def run_standalone_spider(file_name):
        command = 'python ' + logics_dir + f'{file_name}.py'
        os.system(command)

    def run_all_spiders():
        spider_files = [
            'listing_urls_spider',
            'listing_words_spider',
        ]

        for file in spider_files:
            run_standalone_spider(file)

    run_all_spiders()

    input_file = "words_grouped_data.json"

    # with open(logics_dir + input_file, encoding='utf8') as json_data:
    #     words_grouped_data_list = json.load(json_data)

    json_data = s3_resource.Object('test-314e',
                                   f'jsons/{input_file}').get()['Body']

    words_grouped_data_list = json.loads(json_data.read().decode('utf-8'))

    WORDS_GROUPED = words_grouped_data_list

    def data_frequency():
        '''...'''

        groups_of_words_list = WORDS_GROUPED
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
                        word_pair_l.append((words_with_punctuation[i],
                                            next_word))

        return_dict_object = {
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

    output_file = "data_frequency.json"
    data_frequency_dict = data_frequency()

    # with open(logics_dir + output_file, 'w') as json_file:
    #     json.dump(data_frequency_dict, json_file)

    s3_resource.Object(
        'test-314e',
        f'jsons/{output_file}').put(Body=json.dumps(data_frequency_dict))


# execute_all_jobs()


# print(f"\n\nExecuted in {(time.time() - start_time):.2f} seconds.\n")
