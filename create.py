from os import environ
from urlparse import urlparse
import click
import sys

from src.chainspace_client import ChainspaceClient
from src.chainspace_repository import ChainspaceRepository
from chainspacecontract.examples import petition_encrypted as petition_contract
from src.petition import Petition
from read_keys import load_keys

DEFAULT_CHAINSPACE_API_URL = "http://localhost:5000/api/1.0"
DEFAULT_TOR_PROXY_URL = "socks5h://localhost:9050"


class CreateRequestException(Exception):
    def __str__(self):
        return 'Failed to create petition: ' + self.message


def get_chainspace_api_url():
    if 'CHAINSPACE_API_URL' in environ:
        return environ['CHAINSPACE_API_URL']
    return DEFAULT_CHAINSPACE_API_URL


def get_tor_proxy_url():
    if 'TOR_PROXY_URL' in environ:
        return environ['TOR_PROXY_URL']
    return DEFAULT_TOR_PROXY_URL


def createChainspaceClient():
    url = urlparse(get_chainspace_api_url())
    hostname = url.hostname
    port = url.port or 5000
    tor_proxy_url = get_tor_proxy_url()
    return ChainspaceClient(tor_proxy_url, hostname, port)


def petition(key_pair):
    chainspace_repository = ChainspaceRepository(createChainspaceClient(), get_chainspace_api_url())
    return Petition(chainspace_repository, petition_contract, key_pair)


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
