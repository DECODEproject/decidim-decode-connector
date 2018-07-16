from petlib.ec import EcGroup
import click
import sys
from binascii import hexlify
from petlib.pack import encode
import json


def pack(x):
    return hexlify(encode(x))


def setup(nid=713):
    """ generates cryptosystem parameters """
    G = EcGroup(nid)
    g = G.generator()
    hs = [G.hash_to_point(("h%s" % i).encode("utf8")) for i in range(4)]
    o = G.order()
    return (G, g, hs, o)


def key_gen(params):
    """ generate a private / public key pair """
    (G, g, hs, o) = params
    priv = o.random()
    pub = priv * g
    return (priv, pub)


def main(filename):
    try:
        params = setup()
        priv, pub = key_gen(params)

        priv, pub = pack(priv), pack(pub)

        keys = {
            'pub': pub,
            'priv': priv,
        }

        with open(filename, 'w') as fp:
            json.dump(keys, fp)

    except Exception as err:
        print err
        sys.exit(-1)


@click.command()
@click.option('--filename', required=True, help='filename to store the json with the keys')
def cli_main(filename):
    main(filename)


if __name__ == '__main__':
    cli_main()
