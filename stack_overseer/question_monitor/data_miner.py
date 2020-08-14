"""
A data miner uses data_extractor to mine specific data based on given tags.
"""
import re

from stack_overseer.question_monitor.config.api_config import API_KEY
from stack_overseer.question_monitor.data_extractor import Extractor
from stack_overseer.question_monitor.geo_coder import *

DAY = 86400  # exact epoch time for a day


def data_extraction(tag: str):
    """

    :param tag: A stack tag
    :return: Results containing all data from given filters
    """
    page_num = 1  # Start with 1 not 0
    initial_batch = Extractor(api_key=API_KEY, request_type="search", site="stackoverflow",
                              tagged=str(tag), sort="votes",
                              fromdate=int(time.time()) - DAY * 7, todate=int(time.time()),
                              page=page_num, pagesize=100).extract()
    going = True
    data = [initial_batch["items"]]
    while (going):
        page_num += 1
        time.sleep(1)  # dont overload the api endpoint
        question_extractor = Extractor(api_key=API_KEY, request_type="search", site="stackoverflow",
                                       tagged=str(tag), sort="votes",
                                       fromdate=int(time.time()) - DAY * 7, todate=int(time.time()),
                                       page=page_num, pagesize=100)
        question_json = question_extractor.extract()
        if question_json["has_more"] != True:
            # if an api returns has_more it means there are more data
            going = False
        data.append(question_json["items"])
    print("Question count or user count = ", len(data) * 100)  # this number * 100 = question count on "tag"
    return data


def heatmap_parser(tag: str):
    """
    :param tag target tag to mine
    A data miner parsing
    bunch of API responses from stackExchange
    :return:
    """

    def chunks(lst, n):
        """Yield list chunks givn original list and length"""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    data = data_extraction(tag=tag)
    user_table = []

    for each_page in data:
        for each_question in each_page:
            link_string = each_question["owner"]["link"]
            user_id = re.search(r'\d+', link_string).group()  # extract user_ids
            user_table.append(user_id)

    # now we get all user's address. use batch request to get address:

    user_list = list(set(user_table))
    print("unique user count", len(user_list))
    print(user_list)

    # slice users to 100 user chunks for best api quota usage
    sliced_user_list = list(chunks(lst=user_list, n=100))

    address_total_collection = []
    for each_slice in sliced_user_list:
        time.sleep(0.5)
        prepared_query = ";".join(each_slice)
        # now we batch send request
        user_extractor = Extractor(api_key=API_KEY, request_type="user", site="stackoverflow",
                                   user_id=prepared_query)
        user_json = user_extractor.extract()
        # get address collection per slice(100)

        for each_user in user_json["items"]:

            if "location" in each_user:
                address_total_collection.append(each_user["location"])

    # Store the API response to a plain text
    # A database can be utilized here but not necessary
    with open("static/last_week_question_user_address_list.txt", "w", encoding='utf-8') as address_book:
        for each_address in address_total_collection:
            address_book.write(each_address + ";")


def geo_json_batch_generation():
    # Access plain file storage
    with open("static/last_week_question_user_address_list.txt", "r", encoding='utf-8') as address_book:
        address_book_list = address_book.readline()
    address_book_list = address_book_list.split(";")
    address_book_set = list(set(address_book_list))

    address_dict = {}
    for address in address_book_set:
        address.replace("/", "")
        address.replace("%2F", "")
        if not address:
            continue
        address_dict[address] = geo_coder(address)
    result_data_list = []
    for address in address_book_list:
        if not address:
            continue
        result_data_list.append(address_dict[address])

    # Store the Geocoder response to a plain text
    # A database can be utilized here but not necessary.
    with open("static/address_book.txt", "w", encoding='utf-8') as address_book:
        for each_geocode in result_data_list:
            address_book.write(each_geocode[0] + "-" + each_geocode[1] + ";")


def tag_miner(tag: str):
    """
    :param tag target tag to mine
    This is a simple data miner parsing
    bunch of API responses from stackExchange
    :return: a large tag list related to the tag
    """

    DAY = 86400  # exact epoch time for a day
    data = data_extraction(tag=tag)
    tag_table = []
    for each_page in data:
        for each_question in each_page:
            for each_tag in each_question["tags"]:
                tag_table.append(each_tag)

    # Store the taglist response to a plain text
    # A database can be utilized here but not necessary.
    with open("static/last_week_question_tags.txt", "w", encoding='utf-8') as tag_book:
        for each_tag in tag_table:
            tag_book.write(each_tag + ";")


# A simple test
if __name__ == "__main__":
    # do not over test, theres a quota of 10000 daily with token
    # 300 without https://stackapps.com/apps/oauth/
    tag_miner("android")
    # heatmap_parser(tag="android")
    # geo_json_batch_generation()
