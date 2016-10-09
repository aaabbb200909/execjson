from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),
    url(r'^app1/$', 'app1.views.index'),
    url(r'^app1/createjson$', 'app1.views.createjson'),
    url(r'^app1/load$', 'app1.views.load'),
    url(r'^app1/postjson$', 'app1.views.postjson'),
    url(r'^app1/clearcache$', 'app1.views.clearcache'),
    url(r'^app1/dashboard$', 'app1.views.dashboard')

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
