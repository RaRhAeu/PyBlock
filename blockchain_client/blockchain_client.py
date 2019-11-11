import binascii
import Crypto
from Crypto.PublicKey import RSA

from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap

from .transaction import Transaction

app = Flask(__name__)
app.config['SECRET_KEY'] = 'GoAzCIP8jN1MJbjvRI9RzWR4mwOfr9v9GINXga3n_r8'
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/make/transaction')
def make_transaction():
    return render_template('make_transaction.html')


@app.route('/view/transaction')
def view_transaction():
    return render_template('view_transaction.html')


@app.route('/wallet/new', methods=['GET'])
def new_wallet():
    random_gen = Crypto.Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()
    prk = binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii')
    pbk = binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
    response = {
        'private_key': prk,
        'public_key': pbk
    }
    return jsonify(response), 200


@app.route('/generate/transaction', methods=['POST'])
def generate_transaction():
    # TODO: Refactor as a WTFORM and add validators
    sender_address = request.form['sender_address']
    sender_private_key = request.form['sender_private_key']
    recipient_address = request.form['recipient_address']
    value = request.form['amoun']
    transaction = Transaction(
                              sender_address,
                              sender_private_key,
                              recipient_address,
                              value)
    response = {
                'transaction': transaction.to_dict(),
                'signature': transaction.sign_transaction()
                }
    return jsonify(response), 201
