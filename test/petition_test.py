import unittest
import json
from mock import Mock, call
from src.petition import Petition
from src.transaction_log import TransactionLog
from src.exceptions.tally_closed_petition_exception import TallyClosedPetitionException
from src.exceptions.empty_transaction_log_exception import EmptyTransactionLogException
from chainspacecontract.examples.utils import pack
from json import loads


class PetitionTest(unittest.TestCase):

    def setUp(self):
        self.chainspace_repository_mock = Mock()
        self.contract_mock = Mock()
        self.contract_mock.contract = Mock()

        self.key_pair = ("hola fondo norte", "hola fondo sur")
        self.petition = Petition(self.chainspace_repository_mock, self.contract_mock, self.key_pair)

    def test_initialize_petition_should_return_new_petition_object(self):
        init_transaction = {
            'transaction': {
                'outputs': ('petition_token',)
            }
        }
        self.contract_mock.init.return_value = init_transaction

        create_petition_transaction = {
            'transaction': {
                'outputs': ('petition_token', 'new_petition_object')
            }
        }
        self.contract_mock.create_petition.return_value = create_petition_transaction

        output = self.petition.initialize()

        expected_process_transaction_calls = [
            call(init_transaction),
            call(create_petition_transaction)
        ]
        self.chainspace_repository_mock.process_transaction.assert_has_calls(expected_process_transaction_calls, any_order=False)
        self.assertEqual(output, 'new_petition_object')

    def test_get_results_uses_correct_parameters(self):
        inputs = ['new_petition_object']
        no_signatures_transaction_log = loads("""[
            {"transactionJson":{"inputIDs":[],"outputs":["petition_token"],"contractID":"petition_encrypted","methodID":"init"},"timestamp":"2018-04-20 10:57:09.117"},
            {"transactionJson":{"inputIDs":["input_id_for_create_petition"],"outputs":["petition_token","new_petition_object"],"contractID":"petition_encrypted","methodID":"create_petition"},"timestamp":"2018-04-20 10:57:09.653"}
        ]""")
        self.chainspace_repository_mock.get_full_transaction_log.return_value = TransactionLog(no_signatures_transaction_log)
        self.contract_mock.contract.contract_name = 'petition_encrypted'
        expected_output = [0, 0]
        transaction_output = {"outcome": [0, 0, 0, 0, 0, 0], "type": "PetitionEncResult"}
        tally_petition_transaction = {
            'transaction': {
                'outputs': [json.dumps(transaction_output)]
            }
        }
        self.contract_mock.tally.return_value = tally_petition_transaction

        output = self.petition.get_results()

        self.contract_mock.tally.assert_called_with(inputs, self.petition.reference_inputs, self.petition.parameters, pack(self.key_pair[0]), pack(self.key_pair[1]))
        self.chainspace_repository_mock.process_transaction.assert_called_with(tally_petition_transaction)
        self.assertEqual(expected_output, output)

    def test_get_results_returns_correct_result(self):
        inputs = ['new_petition_object']
        no_signatures_transaction_log = loads("""[
            {"transactionJson":{"inputIDs":[],"outputs":["petition_token"],"contractID":"petition_encrypted","methodID":"init"},"timestamp":"2018-04-20 10:57:09.117"},
            {"transactionJson":{"inputIDs":["input_id_for_create_petition"],"outputs":["petition_token","new_petition_object"],"contractID":"petition_encrypted","methodID":"create_petition"},"timestamp":"2018-04-20 10:57:09.653"}
        ]""")
        self.chainspace_repository_mock.get_full_transaction_log.return_value = TransactionLog(no_signatures_transaction_log)
        self.contract_mock.contract.contract_name = 'petition_encrypted'
        expected_output = [3, 2]
        transaction_output = {"outcome": [1, 2, 0, 0, 1, 1], "type": "PetitionEncResult"}
        tally_petition_transaction = {
            'transaction': {
                'outputs': [json.dumps(transaction_output)]
            }
        }
        self.contract_mock.tally.return_value = tally_petition_transaction

        output = self.petition.get_results()

        self.contract_mock.tally.assert_called_with(inputs, self.petition.reference_inputs, self.petition.parameters, pack(self.key_pair[0]), pack(self.key_pair[1]))
        self.chainspace_repository_mock.process_transaction.assert_called_with(tally_petition_transaction)
        self.assertEqual(expected_output, output)

    def test_get_results_returns_an_error_when_there_is_no_petition(self):
        no_transactions = []
        self.chainspace_repository_mock.get_full_transaction_log.return_value = TransactionLog(no_transactions)
        self.contract_mock.contract.contract_name = 'petition_encrypted'
        self.contract_mock.tally.side_effect = Exception("'scores'")

        with self.assertRaises(EmptyTransactionLogException):
            self.petition.get_results()

    def test_get_results_should_raise_exception_if_petition_is_closed(self):
        transaction_log = loads("""[
            {"transactionJson":{"inputIDs":[],"outputs":["petition_token"],"contractID":"petition_encrypted","methodID":"init"},"timestamp":"2018-04-20 10:57:09.117"},
            {"transactionJson":{"inputIDs":["input_id_for_create_petition"],"outputs":["petition_token","new_petition_object"],"contractID":"petition_encrypted","methodID":"create_petition"},"timestamp":"2018-04-20 10:57:09.653"},
            {"transactionJson":{"inputIDs":["input_id_for_tally"],"outputs":["outcome"],"contractID":"petition_encrypted","methodID":"tally"},"timestamp":"2018-04-20 10:58:09.653"}
        ]""")
        self.chainspace_repository_mock.get_full_transaction_log.return_value = TransactionLog(transaction_log)
        self.contract_mock.contract.contract_name = 'petition_encrypted'
        self.contract_mock.tally.side_effect = Exception("'scores'")

        with self.assertRaises(TallyClosedPetitionException):
            self.petition.get_results()

    def test_count_signatures_with_new_petition_returns_count_zero(self):
        no_signatures_transaction_log = loads("""[
            {"transactionJson":{"methodID":"init","inputIDs":[],"outputs":["petition_token"],"contractID":"petition_encrypted"},"timestamp":"2018-04-20 10:57:09.117"},
            {"transactionJson":{"methodID":"create_petition","inputIDs":["input_id_for_create_petition"],"outputs":["petition_token","new_petition_object"],"contractID":"petition_encrypted"},"timestamp":"2018-04-20 10:57:09.653"}
        ]""")
        self.chainspace_repository_mock.get_full_transaction_log.return_value = TransactionLog(no_signatures_transaction_log)
        self.contract_mock.contract.contract_name = 'petition_encrypted'

        output = self.petition.count_signatures()

        expected_output = 0
        self.assertEqual(expected_output, output)

    def test_count_signatures_with_ongoing_petition_returns_correct_count(self):
        transaction_log = loads("""[
            {"transactionJson":{"methodID":"init","inputIDs":[],"outputs":["petition_token"],"contractID":"petition_encrypted"},"timestamp":"2018-04-20 10:57:09.117"},
            {"transactionJson":{"methodID":"create_petition","inputIDs":["input_id_for_create_petition"],"outputs":["petition_token","new_petition_object"],"contractID":"petition_encrypted"},"timestamp":"2018-04-20 10:57:09.653"},
            {"transactionJson":{"methodID":"add_signature","parameters":["[0,1,0,0,0,0]"],"inputIDs":["input_id_for_add_signature"],"outputs":[],"contractID":"petition_encrypted"},"timestamp":"2018-04-20 10:58:09.653"},
            {"transactionJson":{"methodID":"add_signature","parameters":["[1,0,0,0,0,0]"],"inputIDs":["input_id_for_add_signature"],"outputs":[],"contractID":"petition_encrypted"},"timestamp":"2018-04-20 10:58:19.653"},
            {"transactionJson":{"methodID":"add_signature","parameters":["[0,0,0,0,1,0]"],"inputIDs":["input_id_for_add_signature"],"outputs":[],"contractID":"petition_encrypted"},"timestamp":"2018-04-20 10:58:29.653"}
        ]""")
        self.chainspace_repository_mock.get_full_transaction_log.return_value = TransactionLog(transaction_log)
        self.contract_mock.contract.contract_name = 'petition_encrypted'

        output = self.petition.count_signatures()

        expected_output = 3
        self.assertEqual(expected_output, output)

    def test_count_signatures_with_closed_petition_returns_correct_count(self):
        closed_petition_transaction_log = loads("""[
            {"transactionJson":{"methodID":"init","inputIDs":[],"outputs":["petition_token"],"contractID":"petition_encrypted"},"timestamp":"2018-04-20 10:57:09.117"},
            {"transactionJson":{"methodID":"create_petition","inputIDs":["input_id_for_create_petition"],"outputs":["petition_token","new_petition_object"],"contractID":"petition_encrypted"},"timestamp":"2018-04-20 10:57:09.653"},
            {"transactionJson":{"methodID":"add_signature","parameters":["[0,1,0,0,0,0]"],"inputIDs":["input_id_for_add_signature"],"outputs":[],"contractID":"petition_encrypted"},"timestamp":"2018-04-20 10:58:09.653"},
            {"transactionJson":{"methodID":"add_signature","parameters":["[1,0,0,0,0,0]"],"inputIDs":["input_id_for_add_signature"],"outputs":[],"contractID":"petition_encrypted"},"timestamp":"2018-04-20 10:58:19.653"},
            {"transactionJson":{"methodID":"add_signature","parameters":["[0,0,0,0,1,0]"],"inputIDs":["input_id_for_add_signature"],"outputs":[],"contractID":"petition_encrypted"},"timestamp":"2018-04-20 10:58:29.653"},
            {"transactionJson":{"methodID":"tally","inputIDs":["input_id_for_tally"],"outputs":["outcome"],"contractID":"petition_encrypted"},"timestamp":"2018-04-20 10:59:09.653"}
        ]""")
        self.chainspace_repository_mock.get_full_transaction_log.return_value = TransactionLog(closed_petition_transaction_log)
        self.contract_mock.contract.contract_name = 'petition_encrypted'

        output = self.petition.count_signatures()

        expected_output = 3
        self.assertEqual(expected_output, output)
