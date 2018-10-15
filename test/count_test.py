import unittest
import mock
import count


class CountTestCase(unittest.TestCase):

    @mock.patch('count.zenroom_petition')
    def test_count_zenroom_petition_returns_number_of_signatures(self, petition_func_mock):
        number_of_signatures = 3

        petition_mock = mock.Mock()
        petition_mock.count_signatures.return_value = number_of_signatures
        petition_func_mock.return_value = petition_mock

        actual = count.count_signatures()

        self.assertEqual(actual, {'numberOfSignatures': 3})

    @mock.patch('count.zenroom_petition')
    def test_count_zenroom_petition_raises_exception_if_error_counting(self, petition_func_mock):
        petition_mock = mock.Mock()
        petition_mock.count_signatures.side_effect = Exception('')
        petition_func_mock.return_value = petition_mock

        with self.assertRaises(count.CountRequestException):
            actual = count.count_signatures()
