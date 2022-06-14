from math import inf
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, IntegerField, BooleanField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Regexp, EqualTo, Email, InputRequired
from flask_login import current_user
from flask_wtf import FlaskForm
from .db import User



class AddRouteForm(FlaskForm):
    name = StringField('Titel', validators=[DataRequired()])
    description = StringField('Beschreibung', validators=[DataRequired()])
    trail = StringField('GPX-Datei (Pfad)', validators=[DataRequired()])
    previewImage = StringField('Vorschaubild (Pfad)', validators=[DataRequired()])
    technicalDifficulty = IntegerField('Technische Schwierigkeit', validators=[NumberRange(0, 10, 'Es muss ein Wert zwischen 0 (leicht) und 10 (schwer) angegeben werden.')])
    stamina = IntegerField('Ausdauer', validators=[NumberRange(0, 10, 'Es muss ein Wert zwischen 0 (gering) und 10 (hoch) angegeben werden.')])
    distance = IntegerField('Distanz in Meter', validators=[DataRequired(), NumberRange(0, inf, 'Es muss eine Distanz (in Metern) größer als 0 angegeben werden.')])
    duration = IntegerField('Dauer in Minuten', validators=[NumberRange(0, inf, 'Es muss eine Dauer (in Minuten) länger als 0 angegeben werden.')])
    startLon = StringField('Startkoordinate Longitude', validators=[DataRequired(), Regexp('^[\d]{1,3}.[\d]+$', message='Es dürfen nur Zahlen und ein Punkt angegeben werden (12.123123123).')])
    startLat = StringField('Startkoordinate Latitude', validators=[DataRequired(), Regexp('^[\d]{1,3}.[\d]+$', message='Es dürfen nur Zahlen und ein Punkt angegeben werden (12.123123123).')])
    submit = SubmitField('Erstellen')

    def validate(self, extra_validators=None):
        return super().validate(extra_validators)

class RouteDetailsForm(FlaskForm):
    name = StringField('Titel', validators=[DataRequired()])
    description = StringField('Beschreibung', validators=[DataRequired()])
    trail = StringField('GPX-Datei (Pfad)', validators=[DataRequired()])
    previewImage = StringField('Vorschaubild (Pfad)', validators=[DataRequired()])
    technicalDifficulty = IntegerField('Technische Schwierigkeit', validators=[NumberRange(0, 10, 'Es muss ein Wert zwischen 0 (leicht) und 10 (schwer) angegeben werden.')])
    stamina = IntegerField('Ausdauer', validators=[NumberRange(0, 10, 'Es muss ein Wert zwischen 0 (gering) und 10 (hoch) angegeben werden.')])
    distance = IntegerField('Distanz in Meter', validators=[DataRequired(), NumberRange(0, inf, 'Es muss eine Distanz (in Metern) größer als 0 angegeben werden.')])
    duration = IntegerField('Dauer in Minuten', validators=[NumberRange(0, inf, 'Es muss eine Dauer (in Minuten) länger als 0 angegeben werden.')])
    
    # highlights
    addHighlight = SubmitField('Neues Highlight hinzufügen')
    hName = StringField('Highlight Titel', validators=[DataRequired()])
    hDescription = StringField('Highlight Beschreibung', validators=[DataRequired()])
    hPreviewImage = StringField('Highlight Vorschaubild (Pfad)', validators=[DataRequired()])
    longitude = StringField('Longitude', validators=[DataRequired(), Regexp('^[\d]{1,3}.[\d]+$', message='Es dürfen nur Zahlen und ein Punkt angegeben werden (12.123123123).')])
    latitude = StringField('Latitude', validators=[DataRequired(), Regexp('^[\d]{1,3}.[\d]+$', message='Es dürfen nur Zahlen und ein Punkt angegeben werden (12.123123123).')])

    # tags
    addTagOfRoute = SubmitField('Tag für Route hinzufügen')
    tag = StringField('Tag', validators=[DataRequired()])

    # reviews
    addReview = SubmitField('')

    # images
    addRouteImage = SubmitField('Neues Bild für Route hinzufügen')
    routeImage = StringField('Bild von der Route (Pfad)', validators=[DataRequired()])
    addHighlightImage = SubmitField('Neues Bild für Highlight hinzufügen')
    hImage = StringField('Highlight Bild (Pfad)', validators=[DataRequired()])



    submit = SubmitField('Erstellen')

    def validate(self, extra_validators=None):
        return super().validate(extra_validators)


class LoginForm(FlaskForm):
    user_name = StringField('Benutzername', validators=[InputRequired()])
    password = PasswordField('Passwort', validators=[InputRequired()])
    submit = SubmitField('Anmelden')

    def validate(self):     #Extends the validate-function
        if not super(LoginForm, self).validate():
            return False
        user = User.query.filter_by(username=self.user_name.data).first()
        if not user:     # tests if username exists
            self.user_name.errors.append("Ungültige Login-Daten")
            return False
        if user.password != self.password.data:     #Tests if password is correct
            self.password.errors.append('Ungültige Login-Daten')
            return False
        return True


class RegistrationForm(FlaskForm):
    user_name = StringField('Benutzername', validators=[InputRequired()])
    email = StringField(
        'E-Mail Addresse', validators=[Email("Bitte überprüfe die E-Mail-Adresse")])
    password = PasswordField('Passwort', [
        DataRequired(),
        EqualTo('confirm_password', message='Die Passwörter stimmen nicht überein')
    ])
    confirm_password = PasswordField('Passwort', [InputRequired()])
    captcha = BooleanField('Ich bin kein Roboter', [InputRequired()])
    submit = SubmitField("Konto erstellen")

    def validate(self):
        if not super(RegistrationForm, self).validate():
            return False
        user = User.query.filter_by(username=self.user_name.data).first()
        if user:        #Tests, if the username is already assigned
            self.user_name.errors.append("Der Benutzername ist bereits vergeben")
            return False
        return True
        

class AccountSettings(FlaskForm):
    user_name = StringField('Benutzername')
    email = StringField(
        'E-Mail Addresse', validators=[Email("Bitte überprüfe die E-Mail-Adresse")])
    # old_password = PasswordField('Altes Passwort', validators=[DataRequired()])
    new_password = PasswordField('Neues Passwort', [
        EqualTo('confirm_password', message='Die Passwörter stimmen nicht überein')
    ])
    confirm_password = PasswordField('Passwort bestätigen')
    submit = SubmitField("Änderungen speichern")

    def validate(self):
        if not super().validate():
            return False
        if self.user_name.data != current_user.username and User.query.filter_by(username=self.user_name.data).first():
            self.user_name.errors.append("Der Benutzername ist bereits vergeben.")
            return False
        return True