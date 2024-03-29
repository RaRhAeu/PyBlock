import binascii
import Crypto
from Crypto.PublicKey import RSA
import requests
import json

from flask import Flask, render_template, jsonify, flash, redirect, url_for
from flask_bootstrap import Bootstrap

from transaction import Transaction
from transaction_form import TransactionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'GoAzCIP8jN1MJbjvRI9RzWR4mwOfr9v9GINXga3n_r8'
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


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


@app.route('/make/transaction', methods=['GET'])
def make_trans():
    form = TransactionForm()
    return render_template('make_transaction.html', form=form)


@app.route('/generate/transaction', methods=['POST'])
def generate_transaction():
    form = TransactionForm()
    # print('asdsadasads')
    if form.validate_on_submit():
        sender_address = form.sender_address.data
        sender_private_key = form.sender_private_key.data
        recipient_address = form.recipient_address.data
        value = int(form.amount.data)
        transaction = Transaction(
            sender_address, sender_private_key, recipient_address, value
         )
        print(transaction.to_dict())
        res = {'transaction': transaction.to_dict(),
               'signature': transaction.sign_transaction()
               }
        requests.post("http://127.0.0.1:8888/transactions/new",
                      json=res)
        print(res)
        # print('asdsadasads')
        flash('Successfull Transaction!')
    else:
        flash('Incorrect data, try again.')
    return redirect(url_for('make_trans'))


if __name__ == '__main__':
    app.run(debug=True)
