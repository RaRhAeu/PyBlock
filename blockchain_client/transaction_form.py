from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, HiddenField
from wtforms.validators import Required, URL


class TransactionForm(FlaskForm):
    sender_address = StringField('Sender Address: ', validators=[Required()])
    sender_private_key = StringField('Private Key: ', validators=[Required()])
    recipient_address = StringField(
        'Recipient Address: ', validators=[Required()]
        )
    amount = IntegerField('Amount to Send: ')
    node_url = HiddenField(validators=[URL()], default="http://127.0.0.1:8888")
    submit = SubmitField('Submit')
