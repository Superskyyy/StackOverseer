import json
from urllib.parse import urlencode

import requests


class Extractor:
    """
    a extractor class utilizes the StackExchange API https://api.stackexchange.com/docs

    API Version - 2.2
    """

    def __init__(self, api_key: str, request_type: str, site: str, question_id="", **params):
        """
        :param api_key: well this is a api_key to increase my quota
        :param request_type: either search/question/answer
        :param site: usually you want stackoverflow..
        :param params: a list of API doc defined params
        """
        self.question_id = question_id
        self.api_key = api_key
        self.request_params = params
        self.request_type = request_type
        self.content_json = None
        self.api_root = "https://api.stackexchange.com/2.2/"
        self.raw_result = None
        self.request_url = ""
        self.site = site
        self.url_builder()

    def jsonify(self):
        cleaned = self.raw_result.decode('utf8').replace("'", '"')
        data = json.loads(cleaned)
        result = json.dumps(data, indent=4, sort_keys=True)
        # print(result)
        return data

    def url_builder(self):
        # ideally we list ALL api end-points here but im too lazy.
        if self.request_type == "search":
            self.request_url += self.api_root + "search?" + urlencode(self.request_params)

        elif self.request_type == "question_answers":  # get answer by question
            if self.question_id != "":
                self.request_url += self.api_root + "questions/" + self.question_id + "/answers?" + urlencode(
                    self.request_params)
            else:
                print("error")
        elif self.request_type == "answer":  # wont be used
            self.request_url += self.api_root + "answers?" + urlencode(self.request_params)
            pass
        self.request_url += "&site=" + str(self.site)
        self.request_url += "&key=" + str(self.api_key)
        # print(self.request_url)

    def extract(self):

        self.raw_result = requests.get(self.request_url).content
        # print(self.raw_result)
        result = self.jsonify()
        print(f"json_obj: {result}\n\n")
        print(self.request_url)
        return result


# A simple test
if __name__ == "__main__":
    # do not over test, theres a quota of 10000 daily with token
    # 300 without https://stackapps.com/apps/oauth/

    my_extractor = Extractor(api_key="6pOvVEqSzJc2ki6x5q)o6w((", request_type="search", site="stackoverflow",
                             tagged="android", page=1,
                             pagesize=10)

    # my_extractor = Extractor(api_key="???????????????" ,request_type="search", site="stackoverflow", tagged="android", page=1, pagesize=10)
    json_data = my_extractor.extract()

    top_ten = []  # a list of top ten votes
    for each_question in json_data["items"]:
        info_block = [each_question["score"], each_question["link"], each_question["tags"]]
        top_ten.append(info_block)
    print(top_ten)
    question_extractor = Extractor(api_key="6pOvVEqSzJc2ki6x5q)o6w((", request_type="search", site="stackoverflow",
                                   tagged="android", page=1, pagesize=10, sort="votes")
    json_data = my_extractor.extract()
    print(json_data)
    answer_extractor = Extractor(api_key="6pOvVEqSzJc2ki6x5q)o6w((", request_type="question_answers",
                                 site="stackoverflow",
                                 sort="votes", order="desc",
                                 question_id="39727698")
    json_data = answer_extractor.extract()
