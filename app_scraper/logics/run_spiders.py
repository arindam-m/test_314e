import json
import os
import re
import string
import time
from collections import Counter


start_time = time.time()


def execute_all_jobs():

    def run_standalone_spider(file_name):

        cwd = os.getcwd() + '\\app_scraper\\logics\\'
        command = 'python ' + cwd + f'{file_name}.py'
        os.system(command)

    def run_all_spiders():

        spider_files = [
            'listing_urls_spider',
            'listing_words_spider',
        ]

        for file in spider_files:
            run_standalone_spider(file)

    run_all_spiders()

    json_file = os.getcwd() + "\\app_scraper\\logics\\words_grouped_data.json"

    with open(json_file, encoding='utf8') as json_data:
        words_grouped_data_list = json.load(json_data)

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

    output_file = os.getcwd() + "\\app_scraper\\logics\\data_frequency.json"
    data_frequency_dict = data_frequency()

    with open(output_file, 'w') as json_file:
        json.dump(data_frequency_dict, json_file)


# execute_all_jobs()


print(f"\n\nExecuted in {(time.time() - start_time):.2f} seconds.\n")
