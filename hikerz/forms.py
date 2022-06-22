from math import inf
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, IntegerField, BooleanField, PasswordField, TextAreaField, RadioField, FileField
from wtforms.validators import DataRequired, NumberRange, Regexp, EqualTo, InputRequired, Email, ValidationError
from flask_login import current_user
from flask_wtf import FlaskForm
from .db import User
import re



class AddRouteForm(FlaskForm):

    def getStartCoordinates():
        # TODO: read first coords from gpx file -> should maybe add format validation for gpx file

        """
        - read file
        - get first lon and first lat
        - return as tuple
        """

        return ('51.91158819152654', '8.839563053438653') # default: coords of Hermannsdenkmal


    name = StringField('Titel', validators=[DataRequired()])
    description = TextAreaField('Beschreibung', validators=[DataRequired()])

    distance = IntegerField('Distanz in Metern', validators=[DataRequired(), NumberRange(0, inf, 'Es muss eine Distanz (in Metern) größer als 0 angegeben werden.')])
    duration = IntegerField('Dauer in Minuten', validators=[NumberRange(0, inf, 'Es muss eine Dauer (in Minuten) länger als 0 angegeben werden.')])
    technicalDifficulty = RadioField(label='Technische Schwierigkeit', choices=[('1', 'Einfach'), ('2', ''), ('3', ''), ('4', ''), ('5', 'Schwer')], default='1', coerce=int)
    stamina = RadioField(label='Ausdauer', choices=[('1', 'Gering'), ('2', ''), ('3', ''), ('4', ''), ('5', 'Hoch')], default='1', coerce=int)

    # The regular expressions validate the file-paths (especially the types)
    regexGpx = re.compile('^[\w]+\.(gpx|GPX)$')
    trail = FileField(label='GPX-Datei', validators=[Regexp(regexGpx, 'Eine ungültige GPX-Datei wurde ausgewählt!')])
    regexImage = re.compile('^[\w]+\.(jpg|png|jpeg|JPG|JPEG|PNG)$')
    previewImage = FileField(label='Vorschaubild', validators=[Regexp(regexImage, 'Eine ungültige Bild-Datei wurde ausgewählt! (jpg|png|jpeg)')])

    startCoordinates = getStartCoordinates()
    longitude = StringField('Längengrad', default=startCoordinates[0])
    latitude = StringField('Breitengrad', default=startCoordinates[1])
    creator = StringField('Ersteller', default=current_user)

    submit = SubmitField('Route erstellen')

    def validate(self, extra_validators=None):
        return super().validate(extra_validators)


class AddHighlightForm(FlaskForm):
    name = StringField('Highlight Titel', validators=[DataRequired()])
    description = StringField('Highlight Beschreibung', validators=[DataRequired()])
    previewImage = StringField('Highlight Vorschaubild (Pfad)', validators=[DataRequired()])
    longitude = StringField('Längengrad', validators=[DataRequired(), Regexp('^[\d]{1,3}.[\d]+$', message='Es dürfen nur Zahlen und ein Punkt angegeben werden (12.123123123).')])
    latitude = StringField('Breitengrad', validators=[DataRequired(), Regexp('^[\d]{1,3}.[\d]+$', message='Es dürfen nur Zahlen und ein Punkt angegeben werden (12.123123123).')])
    creator = StringField('Ersteller', default=current_user)

    submit = SubmitField('Neues Highlight hinzufügen')


    def validate(self, extra_validators=None):
        return super().validate(extra_validators)


class AddRouteImageForm(FlaskForm):
    regex = re.compile('^[\w]+\.(jpg|png|jpeg|JPG|JPEG|PNG)$')
    image = FileField(label='Routenbild', validators=[Regexp(regex, 'Eine ungültige Bild-Datei wurde ausgewählt! (jpg|png|jpeg)')])
    routeId = StringField()
    creator = StringField(default=current_user)
    # TODO: build path from filename
    submit = SubmitField('Bild hinzufügen')

    def validate(self, extra_validators=None):
        return super().validate(extra_validators)


class AddHighlightImageForm(FlaskForm):
    regex = re.compile('^[\w]+\.(jpg|png|jpeg|JPG|JPEG|PNG)$')
    image = FileField(label='Bild', validators=[Regexp(regex, 'Eine ungültige Bild-Datei wurde ausgewählt! (jpg|png|jpeg)')])
    # TODO: build path from filename
    submit = SubmitField('Bild hinzufügen')

    def validate(self, extra_validators=None):
        return super().validate(extra_validators)

# TODO: Reviews and Tags (postponed)


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
        'E-Mail Addresse', validators=[Email(message="Bitte überprüfe die E-Mail-Adresse")])
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