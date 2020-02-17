"""waferroll URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from . import view, testdb, search, search2, current_datetime, hour_ahead
from django.conf.urls import url
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('hello/', view.hello),
    path('testdb/', testdb.testdb),
    path('search_form/', search.search_form),
    path('search/', search.search),
    #path('search-post/', search2.search_post),
    url(r'^search-post$', search2.search_post),
    url(r'^admin/', admin.site.urls),
    #url(r'^datetime$/', current_datetime.current_datetime),
    path('datetime/', current_datetime.current_datetime),
    url(r'^time/plus/(\d{1,2})/$', hour_ahead.hours_ahead),
]
