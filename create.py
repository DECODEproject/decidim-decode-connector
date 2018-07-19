from urlparse import urlparse
import click
import sys

from src.chainspace_client import ChainspaceClient
from src.chainspace_repository import ChainspaceRepository
from chainspacecontract.examples import petition_encrypted as petition_contract
from src.petition import Petition
from read_keys import load_keys
from petition_builder import petition


class CreateRequestException(Exception):
    def __str__(self):
        return 'Failed to create petition: ' + self.message

def create_petition(key_pair):
    try:
        our_object = petition(key_pair).initialize()

        petitionObjectID = our_object.object_id
        result = {'petitionObjectId': petitionObjectID}

        return result
    except Exception as e:
        raise CreateRequestException(str(e))

def main(keyfile):
    try:
        keys = load_keys(keyfile)
        results = create_petition(keys)

        print "petition created successfully!"
        print results
    except Exception as err:
        print err
        sys.exit(-1)


@click.command()
@click.option('--keyfile', default='/keys/key.json', help='Seed for key generation')
def cli_main(keyfile):
    main(keyfile)


if __name__ == '__main__':
    cli_main()
