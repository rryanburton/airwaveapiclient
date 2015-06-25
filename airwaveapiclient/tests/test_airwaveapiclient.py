# -*- coding: utf-8 -*-

"""UnitTests for airwaveapiclient."""

import unittest
from httmock import all_requests, response, HTTMock
from airwaveapiclient import AirWaveAPIClient


# pylint: disable=unused-argument, too-many-instance-attributes
class UnitTests(unittest.TestCase):

    """Class UnitTests.

    Unit test for airwaveapiclient.

    """

    def setUp(self):
        """Setup."""
        self.username = 'username'
        self.password = 'password'
        self.address = '192.168.1.1'
        self.path_ap_list = 'ap_list.xml'
        self.path_ap_detail = 'ap_detail.xml'
        self.path_client_detail = 'client_detail.xml'
        self.path_rogue_detail = 'rogue_detail.xml'

        self.obj = AirWaveAPIClient(username=self.username,
                                    password=self.password,
                                    address=self.address)

        with HTTMock(UnitTests.content_login):
            self.res = self.obj.login()

    def test_init(self):
        """Test init."""
        self.assertEqual(self.obj.username, self.username)
        self.assertEqual(self.obj.password, self.password)
        self.assertEqual(self.obj.address, self.address)

    def test_api_path(self):
        """Test API path."""
        url = self.obj.api_path(self.path_ap_list)
        self.assertEqual(url, 'https://%s/%s' % (self.address,
                                                 self.path_ap_list))

    def test_id_params(self):
        """Test ID Params."""
        ap_ids = [1, 2, 3]
        params = self.obj.id_params(ap_ids)
        self.assertEqual(params, 'id=1&id=2&id=3')

    def test_urlencode(self):
        """Test urlencode."""
        params = {'mac': '12:34:56:78:90:AB'}
        res = self.obj.urlencode(params)
        self.assertEqual(res, 'mac=12%3A34%3A56%3A78%3A90%3AAB')

    def test_login(self):
        """Test login."""
        self.assertEqual(self.res.status_code, 200)

    def test_ap_list(self):
        """Test ap_list."""
        with HTTMock(UnitTests.content_api):
            res = self.obj.ap_list()
        self.assertEqual(res.status_code, 200)

        url = 'https://%s/%s' % (self.address, self.path_ap_list)
        self.assertEqual(res.url, url)

        with HTTMock(UnitTests.content_api):
            ap_ids = [1, 2, 3]
            res = self.obj.ap_list(ap_ids)
        self.assertEqual(res.status_code, 200)

        params = self.obj.id_params(ap_ids)
        url = 'https://%s/%s?%s' % (self.address,
                                    self.path_ap_list,
                                    params)
        self.assertEqual(res.url, url)

    def test_ap_detail(self):
        """Test ap_detail."""
        with HTTMock(UnitTests.content_api):
            ap_id = 1
            res = self.obj.ap_detail(ap_id)
        self.assertEqual(res.status_code, 200)

        ap_ids = [ap_id]
        params = self.obj.id_params(ap_ids)
        url = 'https://%s/%s?%s' % (self.address,
                                    self.path_ap_detail,
                                    params)
        self.assertEqual(res.url, url)

    def test_client_detail(self):
        """Test client detail."""
        with HTTMock(UnitTests.content_api):
            mac = '12:34:56:78:90:AB'
            params = {'mac': mac}
            params = self.obj.urlencode(params)
            res = self.obj.client_detail(mac)
        self.assertEqual(res.status_code, 200)

        url = 'https://%s/%s?%s' % (self.address,
                                    self.path_client_detail,
                                    params)
        self.assertEqual(res.url, url)

    def test_rogue_detail(self):
        """Test rogue detail."""
        with HTTMock(UnitTests.content_api):
            ap_id = 1
            params = {'id': ap_id}
            params = self.obj.urlencode(params)
            res = self.obj.rogue_detail(ap_id)
        self.assertEqual(res.status_code, 200)

        url = 'https://%s/%s?%s' % (self.address,
                                    self.path_rogue_detail,
                                    params)
        self.assertEqual(res.url, url)

    @staticmethod
    @all_requests
    def content_login(url, request):
        """Test content for login."""
        cookie_key = 'Mercury::Handler::AuthCookieHandler_AMPAuth'
        cookie_val = '01234567890abcdef01234567890abcd'
        headers = {'Set-Cookie': '%s=%s;' % (cookie_key, cookie_val)}
        content = '<html>html content.</html>'
        return response(status_code=200,
                        content=content,
                        headers=headers,
                        request=request)

    @staticmethod
    @all_requests
    def content_api(url, request):
        """Test content for api."""
        headers = {'content-type': 'application/xml'}
        content = 'xml string'
        return response(status_code=200,
                        content=content,
                        headers=headers,
                        request=request)
