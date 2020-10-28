from django.urls import path

from .views import *

app_name = 'post'
urlpatterns = [
    path('about-us/', InfoView.as_view()),
    path('blog/', PostListView.as_view()),
    path('news/', NewsListView.as_view()),
    path('blog/<int:pk>', PostDetail.as_view()),


]
