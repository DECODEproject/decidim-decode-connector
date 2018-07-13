import unittest
import json
from mock import Mock, call
from src.petition import Petition
from src.transaction_log import TransactionLog
from src.exceptions.sign_closed_petition_exception import SignClosedPetitionException
from src.exceptions.tally_closed_petition_exception import TallyClosedPetitionException
from src.exceptions.empty_transaction_log_exception import EmptyTransactionLogException
from json import loads


class PetitionTest(unittest.TestCase):

    def setUp(self):
        self.chainspace_repository_mock = Mock()
        self.contract_mock = Mock()
        self.contract_mock.contract = Mock()

        self.petition = Petition(self.chainspace_repository_mock, self.contract_mock)
        self.key_pair = ("hola fondo norte", "hola fondo sur")

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

    def test_increment_should_add_new_signature_transaction(self):

        transaction_log = loads("""[
            {"transactionJson":{"inputIDs":[],"outputs":["petition_token"],"contractID":"petition_encrypted","methodID":"init"},"timestamp":"2018-04-20 10:57:09.117"},
            {"transactionJson":{"inputIDs":["input_id_for_create_petition"],"outputs":["petition_token","new_petition_object"],"contractID":"petition_encrypted","methodID":"create_petition"},"timestamp":"2018-04-20 10:57:09.653"}
        ]""")
        self.chainspace_repository_mock.get_full_transaction_log.return_value = TransactionLog(transaction_log)

        self.contract_mock.contract.contract_name = 'petition_encrypted'
        self.contract_mock.add_signature.return_value = 'increment_transaction'

        self.chainspace_repository_mock.process_transaction.return_value = 'chainspace_client_response'

        increment_result = self.petition.increment('Yes', 'female', 'any')

        self.chainspace_repository_mock.process_transaction.assert_called_with('increment_transaction')
        self.assertEqual(increment_result, 'chainspace_client_response')

    def test_increment_should_create_transaction_with_vote_yes(self):
        yes_female_any_index = 10
        expected_contract_signature = [0] * 40
        expected_contract_signature[yes_female_any_index] = 1
        yes_female_any = json.dumps(expected_contract_signature)

        inputs = ('new_petition_object',)
        transaction_log = loads("""[
            {"transactionJson":{"inputIDs":[],"outputs":["petition_token"],"contractID":"petition_encrypted","methodID":"init"},"timestamp":"2018-04-20 10:57:09.117"},
            {"transactionJson":{"inputIDs":["input_id_for_create_petition"],"outputs":["petition_token","new_petition_object"],"contractID":"petition_encrypted","methodID":"create_petition"},"timestamp":"2018-04-20 10:57:09.653"}
        ]""")
        self.chainspace_repository_mock.get_full_transaction_log.return_value = TransactionLog(transaction_log)
        self.contract_mock.contract.contract_name = 'petition_encrypted'

        self.petition.increment('Yes', 'female', 'any')

        self.contract_mock.add_signature.assert_called_with(inputs, self.petition.reference_inputs, self.petition.parameters, yes_female_any)

    def test_increment_should_create_transaction_with_vote_no(self):
        no_female_any_index = 30
        expected_contract_signature = [0] * 40
        expected_contract_signature[no_female_any_index] = 1
        no_female_any = json.dumps(expected_contract_signature)

        inputs = ('new_petition_object',)
        transaction_log = loads("""[
            {"transactionJson":{"inputIDs":[],"outputs":["petition_token"],"contractID":"petition_encrypted","methodID":"init"},"timestamp":"2018-04-20 10:57:09.117"},
            {"transactionJson":{"inputIDs":["input_id_for_create_petition"],"outputs":["petition_token","new_petition_object"],"contractID":"petition_encrypted","methodID":"create_petition"},"timestamp":"2018-04-20 10:57:09.653"}
        ]""")
        self.chainspace_repository_mock.get_full_transaction_log.return_value = TransactionLog(transaction_log)
        self.contract_mock.contract.contract_name = 'petition_encrypted'

        self.petition.increment('No', 'female', 'any')

        self.contract_mock.add_signature.assert_called_with(inputs, self.petition.reference_inputs, self.petition.parameters, no_female_any)

    def test_increment_should_raise_exception_with_invalid_vote_option(self):
        inputs = ('new_petition_object',)
        transaction_log = loads("""[
            {"transactionJson":{"inputIDs":[],"outputs":["petition_token"],"contractID":"petition_encrypted","methodID":"init"},"timestamp":"2018-04-20 10:57:09.117"},
            {"transactionJson":{"inputIDs":["input_id_for_create_petition"],"outputs":["petition_token","new_petition_object"],"contractID":"petition_encrypted","methodID":"create_petition"},"timestamp":"2018-04-20 10:57:09.653"}
        ]""")
        self.chainspace_repository_mock.get_full_transaction_log.return_value = TransactionLog(transaction_log)
        self.contract_mock.contract.contract_name = 'petition_encrypted'

        with self.assertRaises(Exception):
            self.petition.increment('Maybe', 'female', 'any')

    def test_increment_should_raise_exception_if_petition_is_closed(self):
        transaction_log = loads("""[
            {"transactionJson":{"inputIDs":[],"outputs":["petition_token"],"contractID":"petition_encrypted","methodID":"init"},"timestamp":"2018-04-20 10:57:09.117"},
            {"transactionJson":{"inputIDs":["input_id_for_create_petition"],"outputs":["petition_token","new_petition_object"],"contractID":"petition_encrypted","methodID":"create_petition"},"timestamp":"2018-04-20 10:57:09.653"},
            {"transactionJson":{"inputIDs":["input_id_for_tally"],"outputs":["outcome"],"contractID":"petition_encrypted","methodID":"tally"},"timestamp":"2018-04-20 10:58:09.653"}
        ]""")
        self.chainspace_repository_mock.get_full_transaction_log.return_value = TransactionLog(transaction_log)
        self.contract_mock.contract.contract_name = 'petition_encrypted'
        self.contract_mock.add_signature.side_effect = Exception("'tally_pub'")

        with self.assertRaises(SignClosedPetitionException):
            self.petition.increment('yes', 'female', 'any')

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

        output = self.petition.get_results(self.key_pair)

        self.contract_mock.tally.assert_called_with(inputs, self.petition.reference_inputs, self.petition.parameters, self.key_pair[0], self.key_pair[1])
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

        output = self.petition.get_results(self.key_pair)

        self.contract_mock.tally.assert_called_with(inputs, self.petition.reference_inputs, self.petition.parameters, self.key_pair[0], self.key_pair[1])
        self.chainspace_repository_mock.process_transaction.assert_called_with(tally_petition_transaction)
        self.assertEqual(expected_output, output)

    def test_get_results_returns_an_error_when_there_is_no_petition(self):
        no_transactions = []
        self.chainspace_repository_mock.get_full_transaction_log.return_value = TransactionLog(no_transactions)
        self.contract_mock.contract.contract_name = 'petition_encrypted'
        self.contract_mock.tally.side_effect = Exception("'scores'")

        with self.assertRaises(EmptyTransactionLogException):
            self.petition.get_results(self.key_pair)

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
            self.petition.get_results(self.key_pair)
