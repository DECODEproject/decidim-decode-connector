from os import environ
from hashlib import sha256
from petlib.bn import Bn
from petlib.ec import EcGroup
from petlib.pack import encode
from binascii import hexlify
import requests
import json
import click
import sys

DEFAULT_WALLET_PROXY_URL = "http://localhost:5010"
DEFAULT_DECIDIM_MOCK_URL = "http://localhost:3040"


class TallyRequestException(Exception):
    def __str__(self):
        return 'Failed to request tally: ' + self.message


class CloseRequestException(Exception):
    def __str__(self):
        return 'Failed to close Decidim petition: ' + self.message


def encode_key(key):
    return hexlify(encode(key))


def generate_keys(seed):
    g = EcGroup().generator()
    private = Bn.from_hex(seed)
    public = private * g
    private = encode_key(private)
    public = encode_key(public)
    return private, public


def get_wallet_proxy_url():
    if 'WALLET_PROXY_URL' in environ:
        return environ['WALLET_PROXY_URL']
    return DEFAULT_WALLET_PROXY_URL


def get_decidim_mock_url():
    if 'DECIDIM_MOCK_URL' in environ:
        return environ['DECIDIM_MOCK_URL']
    return DEFAULT_DECIDIM_MOCK_URL


def request_tally(url, key_pair):
    (private_key, public_key) = key_pair
    try:
        response = requests.post(url + '/tally', json={
            'private_key': private_key,
            'public_key': public_key
        })
    except Exception as e:
        raise TallyRequestException(str(e))

    if response.status_code >= 400:
        raise TallyRequestException(response.json()['error'])

    return json.loads(response.content)


def decidim_close(url, results):
    try:
        response = requests.post(url + '/close', json=results)
    except Exception as e:
        raise CloseRequestException(str(e))

    if response.status_code >= 400:
        raise CloseRequestException(response.text)


def main(seed):
    seed = sha256(seed).hexdigest()
    key_pair = generate_keys(seed)
    wallet_proxy_url = get_wallet_proxy_url()
    decidim_mock_url = get_decidim_mock_url()

    try:
        results = request_tally(wallet_proxy_url, key_pair)
        decidim_close(decidim_mock_url, results)

        print "petition closed successfully!"
        print results
    except Exception as err:
        print err
        sys.exit(-1)


@click.command()
@click.option('--seed', required=True, help='Seed for key generation')
def cli_main(seed):
    main(seed)


if __name__ == '__main__':
    cli_main()
