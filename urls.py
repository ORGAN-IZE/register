from __future__ import unicode_literals

import django.conf
import django.conf.urls
import django.views.generic
import django.contrib.auth.urls
import django.conf
import django.conf.urls.static
import django.conf.urls.i18n
import django.contrib.admin
from django.contrib.auth import views


urlpatterns = [
    django.conf.urls.url(r'^i18n/', django.conf.urls.include('django.conf.urls.i18n')),
    django.conf.urls.url(r'^robots.txt$', django.views.generic.TemplateView.as_view(template_name='robots.txt')),
    django.conf.urls.url(r'^', django.conf.urls.include('registration.urls')),
    django.conf.urls.url(r'^brand/', django.conf.urls.include('cobrand.urls')),
    django.conf.urls.url(r'^admin/', django.conf.urls.include(django.contrib.admin.site.urls)),

    # override the admin password reset flow to use the normal site password
    # reset flow
    django.conf.urls.url(r'^password_reset/$', views.password_reset, name='admin_password_reset'),
    django.conf.urls.url(r'^login/$', django.views.generic.RedirectView.as_view(url='/admin/login')),
    django.conf.urls.url(r'^', django.conf.urls.include('accountsplus.urls')),
    django.conf.urls.url(r'^widget/', django.conf.urls.include('widget.urls')),
]

urlpatterns += django.conf.urls.static.static(
    django.conf.settings.MEDIA_URL,
    document_root=django.conf.settings.MEDIA_ROOT)

if django.conf.settings.DEBUG:
    import debug_toolbar
    urlpatterns += django.conf.urls.url(
            r'^__debug__/', django.conf.urls.include(debug_toolbar.urls)),


django.contrib.admin.site.site_title = 'Register Admin'
django.contrib.admin.site.site_header = 'Register Admin'
django.contrib.admin.site.index_title = 'Home'
django.contrib.admin.site.disable_action('delete_selected')
