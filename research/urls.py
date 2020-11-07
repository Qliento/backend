from django.urls import path

from .views import *

app_name = 'research'
urlpatterns = [
    path('research/', DefaultResearchView.as_view(), name='file-upload'),
    path('researches/<int:pk>/', ResearchDetail.as_view()),
    path('research-upload/', UploadResearchView.as_view()),
    path('research-update/<int:pk>/', UpdateResearchView.as_view()),
    path('filters/', FiltersAPIView.as_view()),
]
