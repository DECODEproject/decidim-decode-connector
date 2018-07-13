from os import environ
from urlparse import urlparse
import click
import json
import sys

from src.chainspace_client import ChainspaceClient
from src.chainspace_repository import ChainspaceRepository
from chainspacecontract.examples import petition_encrypted as petition_contract
from src.petition import Petition

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


def petition():
    chainspace_repository = ChainspaceRepository(createChainspaceClient(), get_chainspace_api_url())
    return Petition(chainspace_repository, petition_contract)


def create_petition():
    try:
        our_object = petition().initialize()

        petitionObjectID = our_object.object_id
        result = {'petitionObjectId': petitionObjectID}

        return result
    except Exception as e:
        raise CreateRequestException(str(e))


def main():
    try:
        results = create_petition()

        print "petition created successfully!"
        print results
    except Exception as err:
        print err
        sys.exit(-1)


@click.command()
def cli_main():
    main()


if __name__ == '__main__':
    cli_main()
