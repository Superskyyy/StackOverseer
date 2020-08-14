"""
Answer to AJAX requests and normal template context handling.
This is the backend business logic of question_monitor app.
Each view provides a interface to render engine.
"""
import html
import time
from collections import Counter

from django.contrib import messages
from django.http import JsonResponse
from django.views.generic.base import TemplateView

from .config.api_config import API_KEY
from .data_extractor import Extractor
from .rss_parser import RSSExtractor

DAY = 86400  # exact epoch time for a day


class TrendingView(TemplateView):
    template_name = "question_monitor/trending.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, "hello http://example.com")
        context['card_loop'] = range(0, 10)
        context['top_ten'] = self.extract_result_parser()
        return context

    def extract_result_parser(self):
        # logic: get 10 top voted questions over the last week.
        question_extractor = Extractor(api_key=API_KEY, request_type="search", site="stackoverflow",
                                       tagged="android", page=1, pagesize=10, sort="votes",
                                       fromdate=int(time.time()) - DAY * 7, todate=int(time.time()))
        question_json = question_extractor.extract()

        top_ten = []  # a list of top ten votes
        for each_question in question_json["items"]:
            title = html.unescape(each_question['title'])
            info_block = [str(each_question["score"]), each_question["link"], each_question["tags"],
                          title, str(each_question['question_id']), str(each_question["answer_count"])]
            top_ten.append(info_block)
        # print(top_ten)
        return top_ten


class LatestView(TemplateView):
    template_name = "question_monitor/latest.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, "hello http://example.com")
        context['card_loop'] = range(0, 10)
        context['top_ten'] = self.extract_result_parser()
        return context

    def extract_result_parser(self):
        # logic: get 10 latest questions over the last week.
        question_extractor = Extractor(api_key=API_KEY, request_type="search", site="stackoverflow",
                                       tagged="android", page=1, pagesize=10, sort="creation")
        question_json = question_extractor.extract()

        top_ten = []  # a list of top ten votes
        for each_question in question_json["items"]:
            title = html.unescape(each_question['title'])
            info_block = [str(each_question["score"]), each_question["link"], each_question["tags"],
                          title, str(each_question['question_id']), str(each_question["answer_count"])]
            top_ten.append(info_block)
        return top_ten


def get_answer(request):
    stack_feed_json = {}
    if request.method == 'GET':
        question_id = str(request.GET.get('question_id'))
        print(question_id)
        # answer_extractor = Extractor(api_key="6pOvVEqSzJc2ki6x5q)o6w((", request_type="question_answers",
        #                              site="stackoverflow",
        #                              sort="votes", order="desc",
        #                              question_id=question_id)
        # question_json = answer_extractor.extract()

        # RSS Extractor
        stack_feed_json = RSSExtractor(question_id=question_id).parse()
    data = {'data': stack_feed_json}
    return JsonResponse(data)


def get_heatmap(request):
    """
    Handle AJAX load

    :param request:
    :return:
    """
    data = {}

    def parse_heat():
        """
        parses heat data from data source, can be modified to use db
        :return:
        """
        with open("question_monitor/static/address_book.txt", "r") as address_book:
            line = address_book.readline()
        address_list = line.split(";")
        result = []
        for each_address in address_list:
            address = each_address.split("|")
            result.append([address[0], address[1], 0.1])
        return result

    if request.method == 'GET':
        data = {'data': parse_heat()}
    return JsonResponse(data)


def get_word_cloud(request):
    """
    Handle AJAX load
    :param request:
    :return:
    """

    def parse_word_cloud():
        """parse word_cloud data from data source"""
        with open("question_monitor/static/last_week_question_tags.txt", "r") as tag_book:
            line = tag_book.readline()
        tag_list = line.split(";")
        result = list(Counter(tag_list).items())

        return result

    data = {}

    if request.method == 'GET':
        data = {'data': parse_word_cloud()}
    return JsonResponse(data)


class HomePageView(TemplateView):
    template_name = "question_monitor/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
