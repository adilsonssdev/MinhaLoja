from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL

class ItemForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    image = StringField('Image URL', validators=[DataRequired(), URL()])
    details = TextAreaField('Description', validators=[DataRequired()])
    price_id = StringField('Stripe Price ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
