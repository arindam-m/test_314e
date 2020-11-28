import re
import string
from collections import Counter, deque

import requests
from bs4 import BeautifulSoup


# url = "https://www.314e.com/"
# level = 1

URL_TRAVERSE_COUNT = 0


def url_crawler(url, level):

    global URL_TRAVERSE_COUNT

    unique_urls = deque([url])
    considilated_urls_list = []

    traverse_index = level - 1

    while len(unique_urls):

        if traverse_index == 0:
            for _ in range(len(unique_urls)):
                url = unique_urls.popleft()
                considilated_urls_list.append(url)
            break

        for _ in range(len(unique_urls)):

            url = unique_urls.popleft()
            considilated_urls_list.append(url)

            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'lxml')

            links_to_ignore = ['#', 'javascript:void(0);', url]
            anchors = soup.find_all('a')

            for anchor in anchors:
                link = anchor['href']
                if (link not in links_to_ignore
                        and link.startswith(url)
                        and link not in unique_urls):
                    unique_urls.append(link)

        traverse_index -= 1


    URL_TRAVERSE_COUNT = len(considilated_urls_list)

    return considilated_urls_list


# -----------------------------------------------------------------------------#


def words_gouped(url, level):

    groups_of_words_list = []

    considilated_urls_list = url_crawler(url, level)

    for url in considilated_urls_list:

        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.content, 'lxml')


        ## Scraping from Span section

        for span_content in soup.find_all('span'):
            if (span_content.text != '') and (span_content.text != '\n'):
                groups_of_words_list.append(span_content.text)


        ## Scraping from Main section

        words_in_paras_list_raw = []

        for main_content in soup.find_all('main'):
            if (main_content.text != '') and (main_content.text != '\n'):
                words_in_paras_list_raw.append(main_content.text)

        words_list_main = []

        for words_para in words_in_paras_list_raw:
            str_list = (re.split(r"[\n\t]", words_para))
            for str_i in str_list:
                if str_i != '' and str_i != ' ':
                    if str_i.endswith(' '):
                        words_list_main.append(str_i[:-1])
                    elif str_i.endswith('...Read More'):
                        words_list_main.append(str_i[:-12])
                        words_list_main.append(str_i[-9:])
                    else:
                        words_list_main.append(str_i)

        groups_of_words_list += words_list_main


    return groups_of_words_list


# -----------------------------------------------------------------------------#


def frequecy_data(url, level):

    groups_of_words_list = words_gouped(url, level)
    single_str = ' '.join(groups_of_words_list)
    single_words = re.findall("([\w+']+)", single_str.lower())


    # print("Top 10 common words and their frequencies")
    # print("-----------------------------------------")
    # for i in range(10):
    #     tuple_value = Counter(single_words).most_common()[i]
    #     word = tuple_value[0]
    #     freq = tuple_value [1]
    #     if word == 'ehr' or word == 'cdr':
    #         word = word.upper()
    #     print(f"{word}\t: {freq}")
    # print("\n\n")


    word_pair_l = []

    for group_of_words in groups_of_words_list:
        words_with_punctuation = group_of_words.lower().split()

        list_of_punctuations  = list(string.punctuation)

        for i in range(len(words_with_punctuation) - 1):
            if words_with_punctuation[i][-1] not in list_of_punctuations:
                next_word = words_with_punctuation[i + 1]
                if next_word[-1] in list_of_punctuations:
                    word_pair_l.append(
                        (words_with_punctuation[i], next_word[:-1]))
                else:
                    word_pair_l.append((words_with_punctuation[i], next_word))


    # print("Top 10 common word-pairs and their frequencies")
    # print("----------------------------------------------")
    # for i in range(10):
    #     tuple_value = Counter(word_pair_l).most_common()[i]
    #     word_pair = tuple_value[0]
    #     freq = tuple_value [1]
    #     print(f"{word_pair[0]} {word_pair[1]}\t: {freq}")
    # print("\n\n")


    return_dict_object = {
        'no_of_urls' : URL_TRAVERSE_COUNT,
        'common_words': [],
        'common_word_pairs': []
    }

    for i in range(10):

        single_word_tuple = Counter(single_words).most_common()[i]
        word = single_word_tuple[0]
        freq = single_word_tuple [1]
        if word == 'ehr' or word == 'cdr':
            word = word.upper()
        return_dict_object['common_words'].append({word: freq})

        word_pair_tuple = Counter(word_pair_l).most_common()[i]
        word_pair = word_pair_tuple[0][0] + ' ' + word_pair_tuple[0][1]
        freq = word_pair_tuple [1]
        return_dict_object['common_word_pairs'].append({word_pair: freq})


    return return_dict_object


# -----------------------------------------------------------------------------#
