import unittest
import json
from mock import Mock, call
from src.zenroom_petition import ZenroomPetition
from chainspacecontract.examples.utils import pack
from json import loads


class ZenroomPetitionTest(unittest.TestCase):

    def setUp(self):
        self.chainspace_repository_mock = Mock()
        self.contract_mock = Mock()
        self.contract_mock.contract = Mock()

        self.keyfile = 'my_file_path.json'
        self.petition = ZenroomPetition(self.chainspace_repository_mock, self.contract_mock, self.keyfile)

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
