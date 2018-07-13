from chainspacecontract import ChainspaceObject


class Transaction(dict):

    def extract_chainspace_objects(self):
        outputs = self['outputs']
        indexes = range(len(outputs))

        chainspace_objects = map(
            lambda i: ChainspaceObject.from_transaction(self, i),
            indexes
        )
        return list(chainspace_objects)
