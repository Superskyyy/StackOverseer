"""
This is the router logic for the question_monitor application
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.index, name="home")

]

urlpatterns += [
    url(r"^$", views.HomePageView.as_view(), name="home"),
    url(r"^question$", views.QuestionView.as_view(), name="question"),
    url("answers/", views.get_answer, name="get_answer")

]
app_name = 'question_monitor'
