import unittest
import responses
import close
import os
import mock
import json


class CloseTestCase(unittest.TestCase):

    def setUp(self):
        self.wallet_proxy_url = 'http://localhost:5010'
        self.wallet_proxy_tally_url = '%s/tally' % (self.wallet_proxy_url)
        self.decidim_mock_url = 'http://localhost:3040'
        self.decidim_mock_close_url = '%s/close' % (self.decidim_mock_url)
        self.key_pair = ("hola fondo norte", "hola fondo sur")
        self.petition_results = {
            "yes": 5,
            "no": 10,
        }

    @responses.activate
    @mock.patch('close.petition')
    def test_request_tally_from_wallet_proxy(self, petition_func_mock):
        tally_response = [10, 5]

        petition_mock = mock.Mock()
        petition_mock.get_results.return_value = tally_response
        petition_func_mock.return_value = petition_mock

        tally = close.request_tally(self.key_pair)

        expected_tally = {
            'yes': 10,
            'no': 5
        }
        self.assertEqual(tally, expected_tally)
        petition_func_mock.assert_called_with(self.key_pair)

    @responses.activate
    def test_post_mock_decidim_result_success(self):
        responses.add(responses.POST, self.decidim_mock_close_url, json={}, status=200)

        close.decidim_close(self.decidim_mock_url, self.petition_results)
        request_sent = responses.calls[0].request

        self.assertEqual(json.loads(request_sent.body), self.petition_results)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_post_mock_decidim_result_status_codes(self):
        responses.add(responses.POST, self.decidim_mock_close_url, json={}, status=500)

        with self.assertRaises(close.CloseRequestException):
            close.decidim_close(self.decidim_mock_url, self.petition_results)

    @responses.activate
    def test_post_mock_decidim_handles_connection_errors(self):
        responses.add(responses.POST, self.decidim_mock_close_url, body=Exception('Connection error'), status=500)

        with self.assertRaises(close.CloseRequestException):
            close.decidim_close(self.decidim_mock_url, self.petition_results)

    @mock.patch.dict(os.environ, {'DECIDIM_MOCK_URL': 'http://prod.decode.com:3040'})
    def test_get_decidim_mock_url_from_environ(self):
        decidim_mock_url = close.get_decidim_mock_url()
        expected = 'http://prod.decode.com:3040'

        self.assertEqual(decidim_mock_url, expected)

    @mock.patch.dict(os.environ, {})
    def test_get_decidim_mock_url_without_env_should_return_default(self):
        decidim_mock_url = close.get_decidim_mock_url()
        expected = close.DEFAULT_DECIDIM_MOCK_URL

        self.assertEqual(decidim_mock_url, expected)

    @responses.activate
    @mock.patch.dict(os.environ, {})
    @mock.patch('close.petition')
    def test_main_final_test_its_the_final_countdown(self, petition_func_mock):
        tally_outcome = [10, 5]

        petition_mock = mock.Mock()
        petition_mock.get_results.return_value = tally_outcome
        petition_func_mock.return_value = petition_mock

        responses.add(responses.POST, self.decidim_mock_close_url, json={}, status=200)

        close.main('./contrib/key.json')

        request_sent = responses.calls[0].request

        expected_outcome = {
            'yes': 10,
            'no': 5
        }
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(json.loads(request_sent.body), expected_outcome)
