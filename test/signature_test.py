import unittest
from src.signature import Signature


class SignatureTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_signature_vote_yes_without_optional_data(self):
        signature = Signature(vote='yes', gender='any', age='any')
        contract_signature = signature.get_contract_signature_representation()

        yes_any_any_index = 0
        expected_contract_signature = [0] * 40
        expected_contract_signature[yes_any_any_index] = 1

        self.assertEquals(contract_signature, expected_contract_signature)

    def test_signature_vote_no_without_optional_data(self):
        signature = Signature(vote='no', gender='any', age='any')
        contract_signature = signature.get_contract_signature_representation()

        no_any_any_index = 20
        expected_contract_signature = [0] * 40
        expected_contract_signature[no_any_any_index] = 1

        self.assertEquals(contract_signature, expected_contract_signature)

    def test_signature_accepts_upper_and_lower_case(self):
        signature = Signature(vote='Yes', gender='Any', age='Any')
        contract_signature = signature.get_contract_signature_representation()

        yes_any_any_index = 0
        expected_contract_signature = [0] * 40
        expected_contract_signature[yes_any_any_index] = 1

        self.assertEquals(contract_signature, expected_contract_signature)

    def test_signature_accepts_optional_data(self):
        signature = Signature(vote='no', gender='undisclosed', age='40+')
        contract_signature = signature.get_contract_signature_representation()

        no_undisclosed_40_index = 39
        expected_contract_signature = [0] * 40
        expected_contract_signature[no_undisclosed_40_index] = 1

        self.assertEquals(contract_signature, expected_contract_signature)
