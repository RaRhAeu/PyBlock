from collections import OrderedDict
import binascii
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5


class Transaction:
    def __init__(self, sender, private_key, recipient, value):
        self.sender = sender
        self.sender_pk = private_key
        self.recipient = recipient
        self.value = value

    def __getattr__(self, attr):
        return self.data[attr]

    # refactor as json.dumps(self.__dict__, sort_keys=True) ?
    def to_dict(self):
        return OrderedDict({'sender:': self.sender,
                            'recipient': self.recipient,
                            'value': self.value})

    def sign_transaction(self):
        """Sign Transaction with a private key"""
        private_key = RSA.importKey(binascii.unhexlify(self.sender_pk))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        # sig = signer.sign()
        # verifier = PKCS1_v1_5.new(private_key.publickey())
        # verified = verifier.verify(h, sig)
        return binascii.hexlify(signer.sign(h)).decode('ascii')

# TODO: rewrite mining as a C/C++ module for performance improvement
