from os import environ
from urlparse import urlparse
import requests
import click
import sys

from src.chainspace_client import ChainspaceClient
from src.chainspace_repository import ChainspaceRepository
from chainspacecontract.examples import petition_encrypted as petition_contract
from src.petition import Petition
from read_keys import load_keys

DEFAULT_CHAINSPACE_API_URL = "http://localhost:5000/api/1.0"
DEFAULT_TOR_PROXY_URL = "socks5h://localhost:9050"
DEFAULT_DECIDIM_MOCK_URL = "http://localhost:3040"


class TallyRequestException(Exception):
    def __str__(self):
        return 'Failed to request tally: ' + self.message


class CloseRequestException(Exception):
    def __str__(self):
        return 'Failed to close Decidim petition: ' + self.message


def get_chainspace_api_url():
    if 'CHAINSPACE_API_URL' in environ:
        return environ['CHAINSPACE_API_URL']
    return DEFAULT_CHAINSPACE_API_URL


def get_tor_proxy_url():
    if 'TOR_PROXY_URL' in environ:
        return environ['TOR_PROXY_URL']
    return DEFAULT_TOR_PROXY_URL


def get_decidim_mock_url():
    if 'DECIDIM_MOCK_URL' in environ:
        return environ['DECIDIM_MOCK_URL']
    return DEFAULT_DECIDIM_MOCK_URL


def createChainspaceClient():
    url = urlparse(get_chainspace_api_url())
    hostname = url.hostname
    port = url.port or 5000
    tor_proxy_url = get_tor_proxy_url()
    return ChainspaceClient(tor_proxy_url, hostname, port)


def petition(key_pair):
    chainspace_repository = ChainspaceRepository(createChainspaceClient(), get_chainspace_api_url())
    return Petition(chainspace_repository, petition_contract, key_pair)


def request_tally(key_pair):
    try:
        outcome = petition(key_pair).get_results()
        return {
            'yes': outcome[0],
            'no': outcome[1]
        }
    except Exception as e:
        raise TallyRequestException(str(e))


def decidim_close(url, results):
    try:
        response = requests.post(url + '/close', json=results)
    except Exception as e:
        raise CloseRequestException(str(e))

    if response.status_code >= 400:
        raise CloseRequestException(response.text)


def main(keyfile):
    try:
        key_pair = load_keys(keyfile)
        decidim_mock_url = get_decidim_mock_url()
        results = request_tally(key_pair)
        decidim_close(decidim_mock_url, results)

        print "petition closed successfully!"
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
