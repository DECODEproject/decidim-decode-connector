import unittest
from src.transaction import Transaction
from chainspacecontract import ChainspaceObject


class TransactionTest(unittest.TestCase):

    def setUp(self):
        transaction_json = {'contractID': 'contract_id', 'outputs': ['1']}
        self.transaction = Transaction(transaction_json)

    def test_extract_chainspace_objects(self):
        chainspace_objects = self.transaction.extract_chainspace_objects()

        self.assertEquals(len(chainspace_objects), 1)
        self.assertIsInstance(chainspace_objects[0], ChainspaceObject)
        self.assertEquals(chainspace_objects[0], '1')
        self.assertIsNotNone(chainspace_objects[0].object_id)
