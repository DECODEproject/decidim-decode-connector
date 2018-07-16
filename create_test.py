import unittest
import responses
import create
import os
import mock


class CreateTestCase(unittest.TestCase):

    def setUp(self):
        self.wallet_proxy_url = 'http://localhost:5010'
        self.wallet_proxy_mock_create_url = '%s/chainspace/petitions' % (self.wallet_proxy_url)

    @mock.patch.dict(os.environ, {'CHAINSPACE_API_URL': 'http://prod.csapi.com:5000'})
    def test_get_chainspace_api_url_from_environ(self):
        chainspace_api_url = create.get_chainspace_api_url()
        expected = 'http://prod.csapi.com:5000'

        self.assertEqual(chainspace_api_url, expected)

    @mock.patch.dict(os.environ, {})
    def test_get_chainspace_api_url_without_env_should_return_default(self):
        chainspace_api_url = create.get_chainspace_api_url()
        expected = create.DEFAULT_CHAINSPACE_API_URL

        self.assertEqual(chainspace_api_url, expected)

    @mock.patch.dict(os.environ, {'TOR_PROXY_URL': 'socks5h://tor:9050'})
    def test_get_tor_proxy_url_from_environ(self):
        tor_proxy_url = create.get_tor_proxy_url()
        expected = 'socks5h://tor:9050'

        self.assertEqual(tor_proxy_url, expected)

    @mock.patch.dict(os.environ, {})
    def test_get_tor_proxy_url_without_env_should_return_default(self):
        tor_proxy_url = create.get_tor_proxy_url()
        expected = create.DEFAULT_TOR_PROXY_URL

        self.assertEqual(tor_proxy_url, expected)

    @mock.patch('create.petition')
    def test_create_petition_returns_petition_object_id(self, petition_func_mock):
        petition_mock = mock.Mock()
        petition_mock.initialize.return_value = mock.Mock(object_id='111')
        petition_func_mock.return_value = petition_mock

        actual = create.create_petition((('priv_key', 'pub_key')))

        self.assertEqual(actual, {'petitionObjectId': '111'})

#    @mock.patch('create.petition')
#    def test_create_petition_raises_exception_if_error_initializing(self, petition_func_mock):
#        petition_mock = mock.Mock()
#        petition_mock.initialize.side_effect = Exception('')
#        petition_func_mock.return_value = petition_mock
#
#        with self.assertRaises(create.CreateRequestException):
#            actual = create.create_petition()
