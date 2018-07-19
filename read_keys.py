import json
from binascii import unhexlify
from petlib.pack import decode


def unpack(x):
    return decode(unhexlify(x))


def load_keys(filename="/keys/key.json"):
    with open(filename, 'r') as fp:
        key = json.load(fp)

        pub = key['pub']
        priv = key['priv']

        pub = unpack(pub)
        priv = unpack(priv)

        return priv, pub
