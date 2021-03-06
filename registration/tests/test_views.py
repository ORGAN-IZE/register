from __future__ import unicode_literals

import os

import mock

import django.test
import django.test.utils
import django.core.mail
import django.conf

from cobrand.models import CobrandCompany
from widget.models import WidgetHost

from .. import views

SESSION_REGISTRATION_CONFIGURATION = 'registration_configuration'
SESSION_STATE = 'register_state'
SESSION_STATE_NAME = 'register_state_name'
SESSION_EMAIL = 'register_email'
SESSION_POSTAL_CODE = 'register_postal_code'
SESSION_ACCEPTS_REGISTRATION = 'register_accepts_registration'
SESSION_REDIRECT_URL = 'register_redirect_url'
SESSION_RESET_FORM = 'register_reset_form'
SESSION_REGISTRATION_UPDATE = 'registration_update'
SESSION_COBRAND_ID = 'cobrand_id'
SESSION_COBRAND_COMPANY_NAME = 'cobrand_company_name'
SESSION_COBRAND_COMPANY_LOGO = 'cobrand_company_logo'
SESSION_COBRAND_ACTIVE = 'cobrand_active'
SESSION_WIDGET_ID = 'widget_id'
SESSION_WIDGET_HOST_URL = 'widget_host_url'
SESSION_REG_SOURCE = 'reg_source'
SESSION_VARIANT_ID = 'variant_id'

TEST_FILENAME = os.path.join(os.path.dirname(__file__), 'test.jpeg')


class StateLookupViewTestCase(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    def test_get_session(self):
        r = self.client.get('/', follow=False)
        self.assertEqual(r.status_code, 200)

        session = self.client.session

        for key in (
                SESSION_EMAIL, SESSION_STATE, SESSION_STATE_NAME, SESSION_POSTAL_CODE, SESSION_REGISTRATION_CONFIGURATION,
                SESSION_ACCEPTS_REGISTRATION, SESSION_REDIRECT_URL, SESSION_REGISTRATION_UPDATE, SESSION_REG_SOURCE,
                SESSION_VARIANT_ID, SESSION_COBRAND_COMPANY_NAME, SESSION_COBRAND_COMPANY_LOGO, SESSION_COBRAND_ACTIVE,
                SESSION_COBRAND_ID, SESSION_WIDGET_HOST_URL, SESSION_WIDGET_ID,):

            self.assertNotIn(key, session, msg='{} exists in session, while it should not.'.format(key))

    def test_cobrand_session(self):
        # Create cobrand registration
        with open(TEST_FILENAME) as test_file:
            data = {
                'company_name': 'Test Company',
                'contact_name': 'Test Contact',
                'contact_email': 'test@example.com',
                'company_logo': test_file,
                'tos': True,
            }
            r = self.client.post('/brand/', data=data)
        cobrand_company_uuid = r.url.split('/')[-2]
        self.assertRedirects(r, '/brand/{}/'.format(cobrand_company_uuid))
        cobrand_company = CobrandCompany.objects.get(uuid=cobrand_company_uuid)

        # Request Start page
        r = self.client.get('/?cobrand_id={}'.format(cobrand_company_uuid), follow=False)
        self.assertEqual(r.status_code, 200)

        session = self.client.session

        for key in (
                SESSION_EMAIL, SESSION_STATE, SESSION_STATE_NAME, SESSION_POSTAL_CODE, SESSION_REGISTRATION_CONFIGURATION,
                SESSION_ACCEPTS_REGISTRATION, SESSION_REDIRECT_URL, SESSION_REGISTRATION_UPDATE, SESSION_REG_SOURCE,
                SESSION_VARIANT_ID, SESSION_WIDGET_HOST_URL, SESSION_WIDGET_ID,):

            self.assertNotIn(key, session, msg='{} exists in session, while it should not.'.format(key))

        self.assertEquals(session[SESSION_COBRAND_ID], cobrand_company_uuid)
        self.assertEquals(session[SESSION_COBRAND_COMPANY_NAME], cobrand_company.company_name)
        self.assertEquals(session[SESSION_COBRAND_ACTIVE], True)
        self.assertEquals(session[SESSION_COBRAND_COMPANY_LOGO], '{}.png'.format(cobrand_company_uuid))

    def test_widget_session(self):
        # Create widget registration
        data = {
            'host_url': 'http://www.example.com',
            'contact_name': 'Test Contact',
            'contact_email': 'test@example.com',
            'tos': True,
        }
        r = self.client.post('/widget/', data=data)

        widget_host_uuid = r.url.split('/')[-2]
        self.assertRedirects(r, '/widget/{}/'.format(widget_host_uuid))
        widget_host = WidgetHost.objects.get(uuid=widget_host_uuid)

        # Request Start page
        r = self.client.get('/?widget_id={}'.format(widget_host_uuid), follow=False)
        self.assertEqual(r.status_code, 200)

        session = self.client.session

        for key in (
                SESSION_EMAIL, SESSION_STATE, SESSION_STATE_NAME, SESSION_POSTAL_CODE, SESSION_REGISTRATION_CONFIGURATION,
                SESSION_ACCEPTS_REGISTRATION, SESSION_REDIRECT_URL, SESSION_REGISTRATION_UPDATE, SESSION_REG_SOURCE,
                SESSION_VARIANT_ID, SESSION_COBRAND_COMPANY_NAME, SESSION_COBRAND_COMPANY_LOGO, SESSION_COBRAND_ACTIVE,
                SESSION_COBRAND_ID,):

            self.assertNotIn(key, session, msg='{} exists in session, while it should not.'.format(key))

        self.assertEquals(session[SESSION_WIDGET_ID], widget_host_uuid)
        self.assertEquals(session[SESSION_WIDGET_HOST_URL], widget_host.host_url)

    def test_reg_source_session(self):
        # Request Start page
        r = self.client.get('/?reg_source=example-co&variant_id=example-A', follow=False)
        self.assertEqual(r.status_code, 200)

        session = self.client.session

        for key in (SESSION_EMAIL, SESSION_STATE, SESSION_STATE_NAME, SESSION_POSTAL_CODE, SESSION_REGISTRATION_CONFIGURATION,
                    SESSION_ACCEPTS_REGISTRATION, SESSION_REDIRECT_URL, SESSION_REGISTRATION_UPDATE, SESSION_COBRAND_COMPANY_NAME,
                    SESSION_COBRAND_COMPANY_LOGO, SESSION_COBRAND_ACTIVE, SESSION_COBRAND_ID,
                    SESSION_WIDGET_HOST_URL, SESSION_WIDGET_ID,):

            self.assertNotIn(key, session, msg='{} exists in session, while it should not.'.format(key))

        self.assertEquals(session[SESSION_REG_SOURCE], 'example-co')
        self.assertEquals(session[SESSION_VARIANT_ID], 'example-A')

    def test_session_cleaning_on_start(self):
        self.client.get('/', follow=False)
        session = self.client.session
        session[SESSION_EMAIL] = 'test@test.com'
        session[SESSION_POSTAL_CODE] = '96003'
        session[SESSION_STATE] = 'CA'
        session[SESSION_STATE_NAME] = 'california'
        session[SESSION_ACCEPTS_REGISTRATION] = True
        session[SESSION_REGISTRATION_CONFIGURATION] = {}

        self.client.get('/', follow=False)
        session = self.client.session
        for key in (SESSION_EMAIL, SESSION_STATE, SESSION_STATE_NAME, SESSION_POSTAL_CODE, SESSION_REGISTRATION_CONFIGURATION,
                    SESSION_ACCEPTS_REGISTRATION, SESSION_REDIRECT_URL, SESSION_REGISTRATION_UPDATE, SESSION_REG_SOURCE,
                    SESSION_VARIANT_ID, SESSION_COBRAND_COMPANY_NAME, SESSION_COBRAND_COMPANY_LOGO, SESSION_COBRAND_ACTIVE,
                    SESSION_COBRAND_ID, SESSION_WIDGET_HOST_URL, SESSION_WIDGET_ID,):

            self.assertNotIn(key, session, msg='{} exists in session, while it should not.'.format(key))


class FBRedirectViewTestCase(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    def test_session_cleaning_on_start(self):
        r = self.client.get('/fb/', follow=False)
        self.assertRedirects(r, '/?reg_source=fb')


class InstagramRedirectViewTestCase(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    def test_instagram(self):
        r = self.client.get('/instagram/', follow=False)
        self.assertRedirects(r, '/?reg_source=instagram')

    def test_insta(self):
        r = self.client.get('/insta/', follow=False)
        self.assertRedirects(r, '/?reg_source=instagram')


class WaitingListFilmRedirectViewTestCase(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    def test_waitinglistfilm(self):
        r = self.client.get('/waitinglistfilm/', follow=False)
        self.assertRedirects(r, '/?reg_source=waitinglistfilm')


@django.test.utils.override_settings(
    CSP_STYLE_SRC='/static/',
    CSP_SCRIPT_SRC='/static/',
    CSP_FONT_SRC='/static/',
    CSP_IMG_SRC='/static/',
    CSP_MEDIA_SRC='/media/',
)
class CSPHeadersTestCase(django.test.TestCase):
    fixtures = ('test_users.json', 'test_companies.json',)

    def test_response_headers_contain_csp(self):
        c = django.test.client.Client()

        response = c.get('/')

        self.assertEqual(200, response.status_code)
        cspHeader = response['Content-Security-Policy']
        self.assertNotEqual(cspHeader, None)
        self.assertIn('script-src', cspHeader)
        self.assertIn('img-src', cspHeader)
        self.assertIn('style-src', cspHeader)
        self.assertIn('font-src', cspHeader)
        self.assertIn('media-src', cspHeader)
