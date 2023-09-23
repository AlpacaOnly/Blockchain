from flask import Flask, render_template, request, redirect, url_for
from main import Blockchain, MerkleTree, Block
import time

app = Flask(__name__)

# Create a blockchain instance
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html', blockchain=blockchain)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']
    transactions = f"{sender} -> {receiver}: {amount}"
    merkle_tree_root = MerkleTree.build_tree([transactions])
    new_block = Block(len(blockchain.chain), blockchain.get_latest_block().hash, int(time.time()), [transactions], merkle_tree_root)
    blockchain.add_block(new_block)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
