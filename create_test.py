import unittest
import responses
import create
import os
import mock


class CreateTestCase(unittest.TestCase):

    def setUp(self):
        self.wallet_proxy_url = 'http://localhost:5010'
        self.wallet_proxy_mock_create_url = '%s/chainspace/petitions' % (self.wallet_proxy_url)

    @mock.patch.dict(os.environ, {'WALLET_PROXY_URL': 'http://prod.decode.com:8080'})
    def test_get_wallet_proxy_url_from_environ(self):
        wallet_proxy_url = create.get_wallet_proxy_url()
        expected = 'http://prod.decode.com:8080'

        self.assertEqual(wallet_proxy_url, expected)

    @mock.patch.dict(os.environ, {})
    def test_get_wallet_proxy_url_without_env_should_return_default(self):
        wallet_proxy_url = create.get_wallet_proxy_url()
        expected = create.DEFAULT_WALLET_PROXY_URL

        self.assertEqual(wallet_proxy_url, expected)

    @responses.activate
    def test_post_mock_wallet_proxy_result_success(self):
        responses.add(responses.POST, self.wallet_proxy_mock_create_url, json={}, status=200)

        create.create_petition(self.wallet_proxy_url)

        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_post_mock_wallet_proxy_result_status_codes(self):
        responses.add(responses.POST, self.wallet_proxy_mock_create_url, status=500)

        with self.assertRaises(create.CreateRequestException):
            create.create_petition(self.wallet_proxy_url)

    @responses.activate
    def test_post_mock_wallet_proxy_handles_connection_errors(self):
        responses.add(responses.POST, self.wallet_proxy_mock_create_url, body=Exception('Connection error'), status=500)

        with self.assertRaises(create.CreateRequestException):
            create.create_petition(self.wallet_proxy_url)
