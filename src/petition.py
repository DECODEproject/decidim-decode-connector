from chainspacecontract.examples.utils import setup, key_gen, pack
from src.exceptions.tally_closed_petition_exception import TallyClosedPetitionException
import json
from hashlib import sha256
from petlib.bn import Bn


class Petition:

    def __init__(self, chainspace_repository, contract):
        self.chainspace_repository = chainspace_repository
        self.contract = contract

        (self.private_key, self.public_key) = self.generate_key_pair()

        self.reference_inputs = None
        self.parameters = None

    def generate_key_pair(self):
        (G, g, hs, o) = setup()
        hash = sha256("alice").hexdigest()
        private = Bn.from_hex(hash)
        public = private * g
        return private, public

    def initialize(self):
        petition_token = self.__initialize_contract()
        new_petition_object = self.__create_petition(petition_token)
        return new_petition_object

    def get_results(self, key_pair):
        (private_key, public_key) = key_pair
        inputs = [self.__get_chainspace_objects_of_last_transaction()[-1]]

        try:
            transaction = self.contract.tally(
                inputs,
                self.reference_inputs,
                self.parameters,
                private_key,
                public_key
            )
        except Exception as err:
            if str(err) == "'scores'":
                raise TallyClosedPetitionException()
            raise

        self.chainspace_repository.process_transaction(transaction)

        outcome = json.loads(transaction['transaction']['outputs'][0])['outcome']

        result_yes = reduce((lambda x, y: x + y), outcome[:len(outcome) / 2])
        result_no = reduce((lambda x, y: x + y), outcome[len(outcome) / 2:])

        return [result_yes, result_no]

    def __initialize_contract(self):
        transaction = self.contract.init()
        self.chainspace_repository.process_transaction(transaction)
        return transaction['transaction']['outputs'][0]

    def __create_petition(self, petition_token):
        inputs = (petition_token,)

        votes = ['YES', 'NO']
        gender = ['ANY', 'M', 'F', 'U']
        age = ['ANY', '0-19', '20-29', '30-39', '40+']
        options = ["%s-%s-%s" % (v, g, a) for v in votes for g in gender for a in age]
        options = json.dumps(options)

        transaction = self.contract.create_petition(
            inputs,
            self.reference_inputs,
            self.parameters,
            options,
            pack(self.private_key),
            pack(self.public_key)
        )
        self.chainspace_repository.process_transaction(transaction)
        return transaction['transaction']['outputs'][1]

    def __get_chainspace_objects_of_last_transaction(self):
        contract_name = self.contract.contract.contract_name

        transaction_log = self.chainspace_repository.get_full_transaction_log()
        contract_transactions = transaction_log.filter_by_contract_name(contract_name)
        last_transaction = contract_transactions.get_last_transaction()
        return last_transaction.extract_chainspace_objects()
