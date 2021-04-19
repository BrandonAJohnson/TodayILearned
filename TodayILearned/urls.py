from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from feed import urls as feed_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(feed_urls, namespace='feed')),
    url('', include('allauth.urls')),
]
