from __future__ import unicode_literals

import django.conf.urls
import django.views.generic

import views


urlpatterns = [
    django.conf.urls.url(r'^$', views.WidgetCreateView.as_view(), name='widget_create'),
    django.conf.urls.url(r'^(?P<uuid>[\w]{21,22})/$', views.WidgetDetailView.as_view(), name='widget_view'),
    django.conf.urls.url(r'^tos/$', django.views.generic.TemplateView.as_view(template_name='widget/tos.html'), name='widget_tos'),
]
