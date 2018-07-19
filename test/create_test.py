import unittest
import responses
import create
import os
import mock
import petition_builder


class CreateTestCase(unittest.TestCase):

    def setUp(self):
        self.wallet_proxy_url = 'http://localhost:5010'
        self.wallet_proxy_mock_create_url = '%s/chainspace/petitions' % (self.wallet_proxy_url)

    @mock.patch('create.petition')
    def test_create_petition_returns_petition_object_id(self, petition_func_mock):
        petition_mock = mock.Mock()
        petition_mock.initialize.return_value = mock.Mock(object_id='111')
        petition_func_mock.return_value = petition_mock

        actual = create.create_petition((('priv_key', 'pub_key')))

        self.assertEqual(actual, {'petitionObjectId': '111'})

    @mock.patch('create.petition')
    def test_create_petition_raises_exception_if_error_initializing(self, petition_func_mock):
        petition_mock = mock.Mock()
        petition_mock.initialize.side_effect = Exception('')
        petition_func_mock.return_value = petition_mock

        with self.assertRaises(create.CreateRequestException):
            actual = create.create_petition(('priv_key', 'pub_key'))
