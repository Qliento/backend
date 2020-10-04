from django.urls import path

from .views import *

app_name = 'research'
urlpatterns = [
    path('research/', ResearchView.as_view()),
    path('research/<int:pk>', ResearchDetail.as_view()),
    

]
