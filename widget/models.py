from __future__ import unicode_literals

import logging

import django.db.models
import django.core.cache
import django.urls
import django.core.validators

import shortuuidfield


logger = logging.getLogger(__name__)


class WidgetHost(django.db.models.Model):
    created_on = django.db.models.DateTimeField(auto_now_add=True)
    updated_on = django.db.models.DateTimeField(auto_now=True)

    uuid = shortuuidfield.ShortUUIDField(auto=True, unique=True, db_index=True)
    contact_email = django.db.models.EmailField()
    contact_name = django.db.models.CharField(max_length=200)
    host_url = django.db.models.CharField(validators=[django.core.validators.URLValidator()], max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Widget Hosts'
        verbose_name = 'Widget Host'

    def __unicode__(self):
        return unicode(self.host_url)

    def get_absolute_url(self):
        return django.urls.reverse_lazy('widget_view', kwargs={'uuid': self.uuid, })
