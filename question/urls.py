from django.urls import path

from .views import *

app_name = 'post'
urlpatterns = [
    path('partnership/', PartnershipView.as_view()),
    path('faq/', QuestionView.as_view()),
    path('feedback/', FeedbackView.as_view()),
    path('have-question/', HaveQuestionView.as_view()),
]
