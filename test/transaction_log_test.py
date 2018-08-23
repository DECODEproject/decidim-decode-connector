import unittest
from src.transaction_log import TransactionLog
from src.exceptions.empty_transaction_log_exception import EmptyTransactionLogException


class TransactionLogTest(unittest.TestCase):

    def setUp(self):
        log = [{'transactionJson': {'contractID': 'good_contract_id', 'methodID': 'init'}, 'timestamp': '2018-01-01 00:00:00.000'},
               {'transactionJson': {'contractID': 'last_contract_id', 'methodID': 'init'}, 'timestamp': '2018-01-03 00:00:00.000'},
               {'transactionJson': {'contractID': 'good_contract_id', 'methodID': 'add_signature'}, 'timestamp': '2018-01-02 00:00:00.000'}]
        self.transaction_log = TransactionLog(log)

    def test_filter_by_contract_name(self):
        good_contract_transaction_log = self.transaction_log.filter_by_contract_name('good_contract_id')

        self.assertEquals(len(good_contract_transaction_log), 2)
        self.assertEquals(len(self.transaction_log), 3)

    def test_filter_by_method_name(self):
        add_signature_transaction_log = self.transaction_log.filter_by_method_name('add_signature')

        self.assertEquals(len(add_signature_transaction_log), 1)
        self.assertEquals(len(self.transaction_log), 3)

    def test_get_last_transaction(self):
        last_transaction = self.transaction_log.get_last_transaction()

        self.assertEquals(last_transaction, {'contractID': 'last_contract_id', 'methodID': 'init'})

    def test_get_last_transaction_should_throw_error_if_empty(self):
        empty_transaction_log = TransactionLog([])

        with self.assertRaises(EmptyTransactionLogException):
            empty_transaction_log.get_last_transaction()
