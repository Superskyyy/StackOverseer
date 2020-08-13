import json

import feedparser


class RSSExtractor:
    """
    a extractor class utilizes the StackExchange RSS

    """

    def __init__(self, question_id="", ):
        """
        :param question_id: well this is a question id got from StackExchange APIs

        """
        self.question_id = question_id
        self.rss_root = "https://stackoverflow.com/feeds/question/"

    def parse(self):
        stack_feed = feedparser.parse(self.rss_root + self.question_id)
        # print('Number of RSS posts :', len(stack_feed.entries))

        # for entry in stack_feed.entries:
        # print('Post Title :', entry.title)
        # print('Post Summary :', entry.summary)
        # print('Post Link :', entry.link)
        data = {"items": []}
        for count, entry in enumerate(stack_feed.entries):
            data_list = [entry.title, entry.summary, entry.link]
            data['items'].append(data_list)
        json_data = json.dumps(data)

        json_data = json.loads(json_data)
        # print(json_data)
        return json_data


# A simple test
if __name__ == "__main__":
    RSSExtractor(question_id="2979860").parse()
