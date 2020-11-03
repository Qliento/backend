from django.urls import path

from .views import *

app_name = 'research'
urlpatterns = [
    path('research/', DefaultResearchView.as_view(), name='file-upload'),
    path('research/<int:pk>', ResearchDetail.as_view()),
    path('research/by-date-asc', ResearchViewFromOldest.as_view()),
    path('research/by-price-desc', ResearchViewFromCheapest.as_view()),
    path('research/by-price-asc', ResearchViewToCheapest.as_view()),
    path('research-upload/', UploadResearchView.as_view()),
    path('research-update/<int:pk>/', UpdateResearchView.as_view()),
    path('filters/', FiltersAPIView.as_view()),
]
