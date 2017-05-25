from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^createjson$', views.createjson, name='createjson'),
    url(r'^load$', views.load, name='load'),
    url(r'^postjson$', views.postjson, name='postjson'),
    url(r'^clearcache$', views.clearcache, name='clearcache'),
    url(r'^dbsave$', views.dbsave, name='dbsave'),
    url(r'^dbload$', views.dbload, name='dbload'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^alertmanager$', views.alertmanager, name='alertmanager')
]

