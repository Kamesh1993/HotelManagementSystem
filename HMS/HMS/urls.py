"""
Definition of urls for HotelFlexProject.
"""

from datetime import datetime
from django.conf.urls import url, include
import django.contrib.auth.views

import app.forms
import app.views

#Uncomment the next lines to enable the admin:
#from django.conf.urls import include
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^register/$',app.views.register,name='register'),
    url(r'^login/$',app.views.login,name='login'),
    url(r'^booking/$',app.views.booking,name='booking'),
    url(r'^logout$',app.views.logout,name='logout'),
    url(r'^roombooking/$',app.views.roombooking,name='roombooking'),
    url(r'^single/$',app.views.single,name='single'),
    url(r'^forgotpassword/$',app.views.forgotpassword,name='forgot'),
    url(r'^double/$',app.views.double,name='double'),
    url(r'^luxury/$',app.views.luxury,name='luxury'),
    url(r'^deluxe/$',app.views.deluxe,name='deluxe'),
    url(r'^executive/$',app.views.executive,name='executive'),
    url(r'^presidential/$',app.views.presidential,name='presidential'),
    url(r'^bookinghistory/$',app.views.bookinghistory,name='history'),
    url(r'^rooms/$',app.views.rooms,name='rooms'),
    url(r'^adminruby/$',app.views.adminruby,name='adminruby'),
    url(r'^adminlogin/$',app.views.adminlogin,name='adminlogin'),
    url(r'^getusers/$',app.views.getusers,name='adminlogin'),
    url(r'^adminbooking/$',app.views.adminbooking,name='adminbooking'),
    url(r'^salesanalysis/$',app.views.salesanalysis,name='salesanalysis'),
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
]
