"""
URL configuration for protoncrm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

from crmproton.views import login, index, info, page404, task_list,\
    task_settings, account, change_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('login/', login, name="loginproton"),
    path('info/<int:task_id>/', info),
    path('task_list/', task_list),
    path('task_list/<str:state_n>/', task_list),
    path('task/<int:task_id>/', task_settings, name="task"),
    path('account/', account),
    path('account/change_password/', change_password, name="change_password"),
    path('', include("crmproton.urls")),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +\
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page404
