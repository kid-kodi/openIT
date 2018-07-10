from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class InterviewForm(FlaskForm):
    requester = StringField('Demandeur', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=140)])
    interviewer = StringField('Intervenant', validators=[DataRequired()])
    actions = TextAreaField('Actions effectuée', validators=[Length(min=0, max=140)])
    date = StringField('Date', validators=[DataRequired()])
    service = SelectField(choices=[], coerce=int, label="Choisir une unité")
    equipment = SelectField(choices=[], coerce=int, label="Choisir un equipement")
    submit = SubmitField('Enregistrer')


class OrderForm(FlaskForm):
    requester = StringField('Demandeur', validators=[DataRequired()])
    service = StringField('Lieu', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=140)])
    interviewer = StringField('Intervenant', validators=[DataRequired()])
    actions = TextAreaField('Actions effectuée', validators=[Length(min=0, max=140)])
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')


class EquipmentForm(FlaskForm):
    category = SelectField(choices=[], coerce=int, label="Choisir une categorie")
    label = SelectField(choices=[], coerce=int, label="Choisir une marque")
    service = SelectField(choices=[], coerce=int, label="Choisir une unité")
    model = StringField('Modèle', validators=[DataRequired()])
    serial = StringField('Numéro de serie')
    name = StringField('Nom')
    description = TextAreaField('Description', validators=[Length(min=0, max=140)])
    submit = SubmitField('Enregistrer')