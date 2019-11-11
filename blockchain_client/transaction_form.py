from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, HiddenField
from wtforms.validators import Required, URL


class TransactionForm(FlaskForm):
    sender_address = StringField('Sender Address: ', validators=[Required()])
    sender_private_key = StringField('Private Key: ', validators=[Required()])
    recipient_address = StringField(
        'Recipient Address: ', validators=[Required()]
        )
    amount = DecimalField("Amount to Send: ", places=2)
    # node_url = HiddenField(validators=[URL()])
    submit = SubmitField('Submit')
