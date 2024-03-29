import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from collections import OrderedDict
import binascii
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import requests


MINING_SENDER = "THE BLOCKCHAIN"
MINING_REWARD = 1
MINING_DIFFICULTY = 1


class Blockchain:
    def __init__(self):
        self.transactions = []
        self.chain = []
        self.nodes = set()
        # random number as a node id
        self.node_id = str(uuid4()).replace('-', '')
        # Genesis block
        self.create_block(0, '00')

    def register_node(self, node_url):
        """Add a new node to the list of nodes"""
        parsed_url = urlparse(node_url)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def verify_transaction(self, sender_address, signature, transaction):
        """
        Verifies transaction signature, checks that signature corresponds
        to transaction signed by the public key (sender_address)
        """
        public_key = RSA.importKey(binascii.unhexlify(sender_address))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA.new(str(transaction).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(signature))

    def submit_transaction(self, sender_address, recipient_address, value,
                           signature):
        """Adds transaction to transaction array if signature is verified"""
        transaction = OrderedDict({
            'sender_address': sender_address,
            'recipient_address': recipient_address,
            'value': value
        })
        if sender_address == MINING_SENDER:
            self.transactions.append(transaction)
            return len(self.chain) + 1
        else:
            transaction_verification = self.verify_transaction(
                sender_address, signature, transaction
            )
            if transaction_verification:
                self.transactions.append(transaction)
            else:
                return False

    def create_block(self, nonce, prievious_hash):
        """Add a block of transactions to the blockchain"""
        block = {
            'block_number': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'nonce': nonce,
            'prievious_hash': prievious_hash
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def hash(self, block):
        """Creates a SHA-256 hash of a block"""
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self):
        """Proof of work algorithm"""
        last_block = self.chain[-1]
        last_hash = self.hash(last_block)
        nonce = 0
        while self.valid_proof(self.transactions, last_hash, nonce) is False:
            nonce += 1

        return nonce

    def valid_proof(self, transaction, last_hash, nonce,
                    difficulty=MINING_DIFFICULTY):
        """
        Check if a hash value satisfies the mining conditions. Is used with
        proof_of_work function.
        """
        guess = f"{transaction}{last_hash}{nonce}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:difficulty] == '0'*difficulty

    # TODO: refactor this shitty implementation
    def valid_chain(self, chain):
        """Check if a blockchain is valid"""
        last_block = chain[0]
        cur_idx = 1
        while cur_idx < len(chain):
            block = chain[cur_idx]
            if block['prievious_hash'] != self.hash(last_block):
                return False

            transactions = block['transactions'][:-1]
            transaction_elements = [
                'sender_address',
                'recipient_address',
                'value'
                ]
            transactions = [
                OrderedDict((k, transaction[k])
                            for k in transaction_elements
                            ) for transaction in transactions
                            ]
            if not self.valid_proof(transactions, block['prievious_hash'],
                                    block['nonce'], MINING_DIFFICULTY):
                return False
            last_block = block
            cur_idx += 1

    def resolve_conflicts(self):
        """
        Resolve conflicts between blockchain's nodes by replacing our chain
        with the longest on in the network.
        """
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
        for node in neighbours:
            # print(f"http://{node}/chain)
            res = requests.get(f"http://{node}/chain")

            if res.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True

        return False
