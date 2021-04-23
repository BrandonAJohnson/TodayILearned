from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from feed import urls as feed_urls
from profiles import urls as profile_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(feed_urls, namespace='feed')),
    path('profile/', include(profile_urls, namespace='profiles')),
    url('', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # this is not safe for production
