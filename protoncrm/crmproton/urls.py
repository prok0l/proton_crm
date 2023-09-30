from django.conf.urls.static import static
from django.template.defaulttags import url
from django.urls import path, include
from django.conf import settings

from . import views

app_name = 'crmproton'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]