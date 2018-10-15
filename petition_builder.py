from os import environ
from src.chainspace_client import ChainspaceClient
from src.chainspace_repository import ChainspaceRepository
from chainspacecontract.examples import zenroom_petition as zenroom_contract
from src.zenroom_petition import ZenroomPetition
from urlparse import urlparse

DEFAULT_CHAINSPACE_API_URL = "http://localhost:5000/api/1.0"
DEFAULT_TOR_PROXY_URL = None


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


def zenroom_petition(keyfile=None):
    chainspace_repository = ChainspaceRepository(createChainspaceClient(), get_chainspace_api_url())
    return ZenroomPetition(chainspace_repository, zenroom_contract, keyfile)
