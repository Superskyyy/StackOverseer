import html
import time

from django.contrib import messages
from django.http import JsonResponse
from django.views.generic.base import TemplateView

from .data_extractor import Extractor
from .rss_parser import RSSExtractor


class HomePageView(TemplateView):
    template_name = "question_monitor/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, "hello http://example.com")
        return context


class TrendingView(TemplateView):
    template_name = "question_monitor/trending.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, "hello http://example.com")
        context['card_loop'] = range(0, 10)
        context['top_ten'] = self.extract_result_parser()
        return context

    def extract_result_parser(self):
        DAY = 86400  # exact epoch time for a day
        # change this to ajax or page lags
        # logic: get 10 top voted questions over the last week.
        question_extractor = Extractor(api_key="6pOvVEqSzJc2ki6x5q)o6w((", request_type="search", site="stackoverflow",
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
        DAY = 86400  # exact epoch time for a day
        # change this to ajax or page lags
        # logic: get 10 top voted questions over the last week.
        question_extractor = Extractor(api_key="6pOvVEqSzJc2ki6x5q)o6w((", request_type="search", site="stackoverflow",
                                       tagged="android", page=1, pagesize=10, sort="creationn")
        question_json = question_extractor.extract()

        top_ten = []  # a list of top ten votes
        for each_question in question_json["items"]:
            title = html.unescape(each_question['title'])
            info_block = [str(each_question["score"]), each_question["link"], each_question["tags"],
                          title, str(each_question['question_id']), str(each_question["answer_count"])]
            top_ten.append(info_block)
        # print(top_ten)
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
