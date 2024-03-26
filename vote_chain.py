from hashlib import sha256  # Import SHA-256 hashing algorithm
import datetime  # Import datetime module for timestamp
import random  # Import random module for generating nonce
from sys import exit  # Import exit function for error handling

candidates = []  # List to store candidate names
voter_code = 0  # Variable to assign unique voter IDs

class Voter():
    """
    Class representing a voter.

    Attributes:
    - name: Name of the voter
    - id: Unique ID of the voter
    - timestamp: Timestamp of the voter creation
    - nonce: Random nonce value
    - key: Hashed key for the voter
    """
    def __init__(self, name, unique_id, timestamp=datetime.datetime.now()):
        self.name = name
        self.id = unique_id
        self.timestamp = timestamp
        self.nonce = random.randint(0, 1000000)  # Generate a random nonce
        self.key = str(self.calculate_key())  # Calculate hashed key for the voter

    # Method to calculate the hashed key for the voter
    def calculate_key(self):
        checksum = str(self.timestamp) + str(self.id) + str(self.nonce) + self.name
        return str(sha256(checksum.encode("utf-8")).hexdigest())

class Vote():
    """
    Class representing a vote.

    Attributes:
    - voter_key: Key of the voter
    - vote_name: Name of the candidate voted for
    """
    def __init__(self, voter_key, vote_name):
        self.voter_key = voter_key
        isValidCandidate = False
        # Check if voted for a valid candidate
        for candidate in candidates:
            # Check case insensitive for candidate names
            if vote_name.lower() == candidate.lower():
                self.vote_name = vote_name
                isValidCandidate = True
        if isValidCandidate == False:
            print("Error : Specify a valid candidate")
            exit(1)  # Exit the program if an invalid candidate is specified

class Block():
    """
    Class representing a block in the blockchain.

    Attributes:
    - vote_name: Name of the vote
    - previousHash: Hash of the previous block
    - timestamp: Timestamp of the block creation
    - hash: Hash of the current block
    - nonce: Nonce for proof of work
    """
    # Constructor for Block class
    def __init__(self, vote_name, previousHash='', timestamp=datetime.datetime.now()):
        self.timestamp = timestamp
        self.vote_name = vote_name
        self.previousHash = previousHash
        self.hash = ''
        self.nonce = 0

    # Method to calculate the hash of the vote
    def calculate_hash(self):
        checksum = str(self.timestamp) + str(self.vote_name) + self.previousHash + str(self.nonce)
        return str(sha256(checksum.encode("utf-8")).hexdigest())

    # Method for proof of work (mining) of a block
    def validate_block(self, difficulty):
        start_string = ''
        for i in range(difficulty):
            start_string += '0'
        while self.hash[:difficulty] != start_string:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("Block Validated: " + self.hash)

class BlockChain():
    """
    Class representing a blockchain.

    Attributes:
    - chain: List to store blocks in the blockchain
    - difficulty: Difficulty level for mining
    - unvalidated_blocks: List to store unvalidated blocks
    - previouslyVoted: List to track voters who have already voted
    - vote_count: Dictionary to store vote counts for each candidate
    - candidatesInitialized: Flag to ensure candidates initialization
    """
    def __init__(self):
        # Initialize the blockchain with a genesis block
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2  # Difficulty level for mining
        self.unvalidated_blocks = []  # List to store unvalidated blocks
        self.previouslyVoted = []  # List to track voters who have already voted
        self.vote_count = dict()  # Dictionary to store vote counts for each candidate
        self.candidatesInitialized = False  # Flag to ensure candidates initialization

    # Method to create the genesis block
    def create_genesis_block(self):
        genesis = Block("Genesis", "0")
        genesis.hash = genesis.calculate_hash()
        return genesis

    # Method to validate unvalidated blocks and add them to the blockchain
    def validate_unvalidated_blocks(self):
        for vote_name in self.unvalidated_blocks:
            vote_name.validate_block(self.difficulty)
            print("Block validated: " + vote_name.hash)
            self.chain.append(vote_name)

    # Method to create a new block for a given vote_name
    def create_block(self, vote_name):
        if self.candidatesInitialized == False:
            # Initialize vote count dictionary if not already initialized
            self.candidatesInitialized = True
            for candidate in candidates:
                self.vote_count[candidate] = 0
        if str(vote_name.voter_key) in self.previouslyVoted:
            print("Error...a voter can only vote once!")
            exit(1)
        else:
            self.previouslyVoted.append(str(vote_name.voter_key))
            self.vote_count[vote_name.vote_name] += 1
            self.unvalidated_blocks.append(Block(vote_name))

    # Method to get the current vote counts
    def get_votes(self):
        print(self.vote_count)
        return self.vote_count

    # Method to validate the integrity of the blockchain
    def is_chain_valid(self):
        for i in range(1, len(self.chain), 1):
            c_block = self.chain[i]  # Current block
            p_block = self.chain[i - 1]  # Previous block

            # Check if block hash matches the calculated hash
            if c_block.hash != c_block.calculate_hash():
                return False

            # Check if previousHash of current block matches the hash of the previous block
            if c_block.previousHash != p_block.hash:
                return False

        return True
