from django.urls import path

from .views import *
from registration.views import DownloadDemoView

app_name = 'research'
urlpatterns = [
    path('research/', DefaultResearchView.as_view(), name='file-upload'),
    path('update-discount/<int:pk>/', UpdateDiscountPrice.as_view()),
    path('researches/<int:pk>/', ResearchDetail.as_view()),
    path('research-upload/', UploadResearchView.as_view()),
    # path('research-update/<int:pk>/', UpdateResearchView.as_view()),
    path('my-research/<int:pk>/', ResearchOfPartnerDetail.as_view()),
    path('download-demo/<int:pk>/', DownloadDemoView.as_view()),
    path('filters/', FiltersAPIView.as_view()),
]
