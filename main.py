import hashlib
import time

# Define the Block class
class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, merkle_root):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.merkle_root = merkle_root
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.index) + self.previous_hash + str(self.timestamp) + str(self.transactions) + self.merkle_root + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

# Define the Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2  # Adjust the difficulty as needed

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        # Proof of work (basic difficulty requirement)
        while new_block.hash[:self.difficulty] != "0" * self.difficulty:
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

# Define a simple MerkleTree class
class MerkleTree:
    @staticmethod
    def build_tree(transactions):
        if len(transactions) == 0:
            return None
        if len(transactions) == 1:
            return transactions[0]
        new_transactions = []
        for i in range(0, len(transactions), 2):
            if i + 1 < len(transactions):
                combined_hash = hashlib.sha256((transactions[i] + transactions[i + 1]).encode()).hexdigest()
                new_transactions.append(combined_hash)
            else:
                new_transactions.append(transactions[i])
        return MerkleTree.build_tree(new_transactions)

# Example usage:
blockchain = Blockchain()

# Create some sample transactions
transactions = ["Transaction1", "Transaction2", "Transaction3", "Transaction4"]

# Build the Merkle tree from transactions
merkle_tree_root = MerkleTree.build_tree(transactions)

# Create a new block and add it to the blockchain
new_block = Block(len(blockchain.chain), blockchain.get_latest_block().hash, int(time.time()), transactions, merkle_tree_root)
blockchain.add_block(new_block)

# Print the blockchain
for block in blockchain.chain:
    print(f"Block {block.index}:")
    print(f"Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Transactions: {block.transactions}")
    print(f"Merkle Root: {block.merkle_root}")
    print(f"Nonce: {block.nonce}")
    print()

# Output the Merkle root of the last block in the blockchain
print(f"Merkle Root of the Latest Block: {blockchain.get_latest_block().merkle_root}")

def main():
    blockchain = Blockchain()
    while True:
        print("\nBlockchain Menu:")
        print("1. Add Transaction")
        print("2. View Blockchain")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            sender = input("Enter sender: ")
            receiver = input("Enter receiver: ")
            amount = input("Enter amount: ")
            transactions = f"{sender} -> {receiver}: {amount}"
            merkle_tree_root = MerkleTree.build_tree([transactions])
            new_block = Block(len(blockchain.chain), blockchain.get_latest_block().hash, int(time.time()), [transactions], merkle_tree_root)
            blockchain.add_block(new_block)
            print("Transaction added successfully!")
        elif choice == "2":
            for block in blockchain.chain:
                print(f"\nBlock {block.index}:")
                print(f"Hash: {block.hash}")
                print(f"Previous Hash: {block.previous_hash}")
                print(f"Transactions: {block.transactions}")
                print(f"Merkle Root: {block.merkle_root}")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
