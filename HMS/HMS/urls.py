from datetime import datetime
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
import django.contrib.auth.views
import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^register/$',app.views.register,name='register'),
    url(r'^login/$',app.views.login,name='login'),
    url(r'^booking/$',app.views.booking,name='booking'),
    url(r'^logout$',app.views.logout,name='logout'),
    url(r'^events/$',app.views.events,name='events'),
    url(r'^roombooking/$',app.views.roombooking,name='roombooking'),
    url(r'^single/$',app.views.single,name='roombooking'),
    url(r'^double/$',app.views.double,name='roombooking'),
    url(r'^luxury/$',app.views.luxury,name='roombooking'),
    #Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #Uncomment the next line to enable the admin:
    url(r'^admin', admin.site.urls),
]
