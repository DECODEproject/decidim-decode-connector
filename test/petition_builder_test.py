import unittest
import responses
import create
import os
import mock
import petition_builder


class PetitionBuilderTestCase(unittest.TestCase):
    @mock.patch.dict(os.environ, {'CHAINSPACE_API_URL': 'http://prod.csapi.com:5000'})
    def test_get_chainspace_api_url_from_environ(self):
        chainspace_api_url = petition_builder.get_chainspace_api_url()
        expected = 'http://prod.csapi.com:5000'

        self.assertEqual(chainspace_api_url, expected)

    @mock.patch.dict(os.environ, {})
    def test_get_chainspace_api_url_without_env_should_return_default(self):
        chainspace_api_url = petition_builder.get_chainspace_api_url()
        expected = petition_builder.DEFAULT_CHAINSPACE_API_URL

        self.assertEqual(chainspace_api_url, expected)

    @mock.patch.dict(os.environ, {'TOR_PROXY_URL': 'socks5h://tor:9050'})
    def test_get_tor_proxy_url_from_environ(self):
        tor_proxy_url = petition_builder.get_tor_proxy_url()
        expected = 'socks5h://tor:9050'

        self.assertEqual(tor_proxy_url, expected)

    @mock.patch.dict(os.environ, {})
    def test_get_tor_proxy_url_without_env_should_return_default(self):
        tor_proxy_url = petition_builder.get_tor_proxy_url()
        expected = petition_builder.DEFAULT_TOR_PROXY_URL

        self.assertEqual(tor_proxy_url, expected)
