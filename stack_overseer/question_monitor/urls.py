"""
This is the router logic for the question_monitor application
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.index, name="home")

]

# urls from question_monitor application
urlpatterns += [
    url(r"^$", views.HomePageView.as_view(), name="home"),
    url(r"^trending$", views.TrendingView.as_view(), name="trending"),
    url(r"^latest$", views.LatestView.as_view(), name="latest"),
    url("answers/", views.get_answer, name="get_answer"),
    url("heatmap/", views.get_heatmap, name="get_heatmap"),
    url("wordcloud/", views.get_word_cloud, name="get_word_cloud"),

]
app_name = 'question_monitor'
