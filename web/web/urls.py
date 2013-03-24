from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from biomembrane import views as view
import registration

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^web/', include('web.foo.urls')),

    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/icon.ico'}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^$', view.home, name='home'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls'), name='accounts'),
    url(r'^program/', view.program, name='program'),
    url(r'^home/', view.home, name='home'),
    url(r'^rgb_upload/', view.rgb_upload, name='rgb_upload'),
    url(r'results', view.results),
    url(r'batchmode', view.batch, name='batchmode'),
    url(r'triple/setRes/', view.tripleSetRes, name='tripleSetRes'),
    url(r'triple/setParams/', view.tripleSetParams, name='tripleParams'),
)
