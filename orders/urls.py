from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('order-form/', OrderFormCreateView.as_view()),
    path('orders/', OrderCreateView.as_view()),
    path('my-orders/', MyOrdersView.as_view()),

    path('add-to-cart/', AddToCartView.as_view()),
    path('cart/', ItemInCartView.as_view()),
    path('delete-from-cart/<int:pk>/', ItemCartDeleteView.as_view()),

    path('verify-check/', get_paybox_url),

    path('send-demo/', SendDemoView.as_view()),
    path('download/<int:id>/', DownloadFileView.as_view()),

    path('short-descriptions/', ShortDescriptionView.as_view()),

    path('statistics/<int:exact_research>/<int:choice>/', StatViewForResearch.as_view())

]
