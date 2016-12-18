from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^createjson$', views.index, name='createjson'),
    url(r'^load$', views.index, name='load'),
    url(r'^postjson$', views.index, name='postjson'),
    url(r'^clearcache$', views.index, name='clearcache'),
    url(r'^dashboard$', views.index, name='dashboard')
]

