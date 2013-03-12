from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from biomembrane import views as view
import registration

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^web/', include('web.foo.urls')),

    #url(r'/', view.home),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^program/', view.program),
    url(r'^home/', view.home),
)
