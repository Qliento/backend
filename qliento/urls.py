"""qliento URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .router import router
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS

    path('admin/', admin.site.urls),
    path('', include('post.urls')),
    path('', include('research.urls')),
    path('', include(router.urls)),
<<<<<<< HEAD

    path('users/', include('registration.urls')),
    path('purchase/', include('orders.urls')),

    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),


=======
    path('', include('main.urls')),
    path('', include('question.urls')),
>>>>>>> dfc6c994a5d55bfc329e0233ad1e7a1ea05e8267
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
