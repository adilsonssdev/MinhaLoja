from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FloatField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, URL


class ItemForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    image_file = FileField(
        "Upload Image (or provide URL below)",
        validators=[FileAllowed(["jpg", "jpeg", "png", "gif"], "Images only!")],
    )
    image_url = StringField(
        "Or Image URL",
        validators=[Optional(), URL()],
    )
    details = TextAreaField("Description", validators=[DataRequired()])
    price_id = StringField("Stripe Price ID", validators=[Optional()])
    submit = SubmitField("Submit")
