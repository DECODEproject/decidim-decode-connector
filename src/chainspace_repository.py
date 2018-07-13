from json import loads
from src.transaction_log import TransactionLog


class ChainspaceRepository:

    def __init__(self, client, cs_url):
        self.client = client
        self.cs_url = cs_url

    def process_transaction(self, transaction):
        response = self.client.process_transaction(transaction)
        if response.status_code != 200:
            raise Exception('Failed to process transaction for method: ' + transaction['transaction']['methodID'])

        response = loads(response.content)

        if response['success'] != "True":
            raise Exception('Failed to process transaction outcome %s' % response['outcome'])

        return response

    def get_full_transaction_log(self):
        response = self.client.get_transaction_log()

        if response.status_code != 200:
            return {
                'error': "failed to call cs api - " + response.status_code + " : " + response.content
            }

        return TransactionLog(response.json())
