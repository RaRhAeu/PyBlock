from uuid import uuid4

MINING_SENDER = "THE BLOCKCHAIN"
MINING_REWARD = 1
MINING_DIFFICULTY = 2


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
        pass

    def verify_transaction(self, sender_address, signature, transaction):
        """
        Verifies transaction signature, checks that signature corresponds
        to transaction signed by the public key (sender_address)
        """
        pass

    def submit_transaction(self, sender_address, recipient_address, value,
                           signature):
        """Adds transaction to transaction array if signature is verified"""
        pass

    def create_block(self, nonce, prev_hash):
        """Add a block of transactions to the blockchain"""
        pass

    def hash(self, block):
        """Creates a SHA-256 hash of a block"""
        pass

    def proof_of_work(self):
        """Proof of work algorithm"""
        pass

    def valid_proof(self, transaction, last_hash, nonce,
                    difficulty=MINING_DIFFICULTY):
        """
        Check if a hash value satisfies the mining conditions. Is used with
        proof_of_work function.
        """
        pass

    def resolve_conflicts(self):
        """
        Resolve conflicts between blockchain's nodes by replacing our chain
        with the longest on in the network.
        """
