import re

from stack_overseer.question_monitor.config.api_config import API_KEY
from stack_overseer.question_monitor.data_extractor import Extractor
from stack_overseer.question_monitor.geo_coder import *


def heatmap_parser(tag: str):
    """
    :param tag target tag to mine
    This is a simple data miner parsing
    bunch of API responses from stackExchange
    :return:
    """

    DAY = 86400  # exact epoch time for a day
    page_num = 1
    initial_batch = Extractor(api_key=API_KEY, request_type="search", site="stackoverflow",
                              tagged=str(tag), sort="votes",
                              fromdate=int(time.time()) - DAY * 7, todate=int(time.time()),
                              page=page_num, pagesize=100).extract()
    going = True
    data = [initial_batch["items"]]
    while (going == True):
        page_num += 1
        time.sleep(1)  # dont overload the api endpoint
        question_extractor = Extractor(api_key=API_KEY, request_type="search", site="stackoverflow",
                                       tagged=str(tag), sort="votes",
                                       fromdate=int(time.time()) - DAY * 7, todate=int(time.time()),
                                       page=page_num, pagesize=100)
        question_json = question_extractor.extract()
        if question_json["has_more"] != True:
            going = False
        data.append(question_json["items"])
    print("question count /user count", len(data))  # this number * 100 = question count on "tag"
    user_table = []
    for each_page in data:
        for each_question in each_page:
            link_string = each_question["owner"]["link"]
            user_id = re.search(r'\d+', link_string).group()
            user_table.append(user_id)
    # now we get all user's geolocation.
    # first use batch request to get address:
    user_list = list(set(user_table))
    print("unique user", len(user_list))
    print(user_list)

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    sliced_user_list = list(chunks(lst=user_list, n=100))

    address_total_collection = []
    for each_slice in sliced_user_list:
        print("this is a slice", each_slice)
        time.sleep(1)
        prepared_query = ";".join(each_slice)
        # now we batch send request
        user_extractor = Extractor(api_key=API_KEY, request_type="user", site="stackoverflow",
                                   user_id=prepared_query)
        user_json = user_extractor.extract()
        # get address collection per slice(100)

        for each_user in user_json["items"]:

            if "location" in each_user:
                address_total_collection.append(each_user["location"])

    print(address_total_collection, )
    print(len(address_total_collection), len(set(address_total_collection)))
    with open("last_week_question_user_address_list.txt", "w", encoding='utf-8') as address_book:
        for each_address in address_total_collection:
            address_book.write(each_address + ";")


def geo_json_batch_generation():
    # I choose not to use a database cas theres no need..
    with open("last_week_question_user_address_list.txt", "r", encoding='utf-8') as address_book:
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
    with open("address_book.txt", "w", encoding='utf-8') as address_book:
        for each_geocode in result_data_list:
            address_book.write(each_geocode[0] + "-" + each_geocode[1] + ";")

    print(result_data_list)


# A simple test
if __name__ == "__main__":
    # do not over test, theres a quota of 10000 daily with token
    # 300 without https://stackapps.com/apps/oauth/

    # heatmap_parser(tag="android")
    geo_json_batch_generation()
