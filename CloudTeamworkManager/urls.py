"""
CloudTeamworkManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

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

# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
import notifications.urls
import xadmin

urlpatterns = [
    # Uncomment the next line to enable the admin:
    path('xadmin/', xadmin.site.urls),
    path('account/', include('account.urls')),
    path('task/', include('task.urls')),
    path('publisher/', include('publisher.urls')),
    path('file/', include('file.urls')),
    path('noti/', include('noti.urls')),
    path('', include('account.urls')),
    path('favicon.ico/', RedirectView.as_view(url='/static/pic/favicon.ico')),
]
