from math import inf
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, IntegerField, BooleanField, PasswordField, TextAreaField, RadioField, FileField
from wtforms.validators import DataRequired, NumberRange, Regexp, EqualTo, InputRequired, Email, ValidationError
from flask_login import current_user
from flask_wtf import FlaskForm
from .db import User
import re



class AddRouteForm(FlaskForm):
    name = StringField('Titel', validators=[DataRequired()])
    description = TextAreaField('Beschreibung', validators=[DataRequired()])

    distance = IntegerField()
    duration = IntegerField('Dauer in Minuten', validators=[NumberRange(0, inf, 'Es muss eine Dauer (in Minuten) länger als 0 angegeben werden.')])
    technicalDifficulty = RadioField(label='Technische Schwierigkeit', choices=[('1', 'Einfach'), ('2', ''), ('3', ''), ('4', ''), ('5', 'Schwer')], default='1', coerce=int)
    stamina = RadioField(label='Ausdauer', choices=[('1', 'Gering'), ('2', ''), ('3', ''), ('4', ''), ('5', 'Hoch')], default='1', coerce=int)

    # The regular expressions validate the file-paths (especially the types)
    regexGpx = re.compile('^[\w]+\.(gpx|GPX)$')
    trail = FileField(label='GPX-Datei', name='trail', validators=[Regexp(regexGpx, 'Eine ungültige GPX-Datei wurde ausgewählt!'), DataRequired()])
    regexImage = re.compile('^[\w]+\.(jpg|png|jpeg|JPG|JPEG|PNG)$')
    previewImage = FileField(label='Vorschaubild', name='previewImage', validators=[Regexp(regexImage, 'Eine ungültige Bild-Datei wurde ausgewählt! (jpg|png|jpeg)'), DataRequired()])

    longitude = StringField()
    latitude = StringField()

    submit = SubmitField('Route erstellen')

    def validate(self, extra_validators=None):
        return super().validate(extra_validators)


class AddHighlightForm(FlaskForm):
    name = StringField('Titel', validators=[DataRequired()])
    description = StringField('Beschreibung', validators=[DataRequired()])
    regex = re.compile('^[\w]+\.(jpg|png|jpeg|JPG|JPEG|PNG)$')
    previewImage = FileField(label='Vorschaubild', name='highlightPreviewImage', validators=[Regexp(regex, 'Eine ungültige Bild-Datei wurde ausgewählt! (jpg|png|jpeg)'), DataRequired()])
    creator = StringField('Ersteller', default=current_user)

    submit = SubmitField('Neues Highlight hinzufügen')


    def validate(self, extra_validators=None):
        return super().validate(extra_validators)


class AddRouteImageForm(FlaskForm):
    regex = re.compile('^[\w]+\.(jpg|png|jpeg|JPG|JPEG|PNG)$')
    image = FileField(label='Routenbild', name='routeImage', validators=[Regexp(regex, 'Eine ungültige Bild-Datei wurde ausgewählt! (jpg|png|jpeg)'), DataRequired()])
    routeId = StringField()
    creator = StringField(default=current_user)

    submit = SubmitField('Neues Bild hinzufügen')

    def validate(self, extra_validators=None):
        return super().validate(extra_validators)


class AddHighlightImageForm(FlaskForm):
    regex = re.compile('^[\w]+\.(jpg|png|jpeg|JPG|JPEG|PNG)$')
    image = FileField(label='Bild', validators=[Regexp(regex, 'Eine ungültige Bild-Datei wurde ausgewählt! (jpg|png|jpeg)'), DataRequired()])
    submit = SubmitField('Bild hinzufügen')

    def validate(self, extra_validators=None):
        return super().validate(extra_validators)


class LoginForm(FlaskForm):
    """WTForm class for the login form. Author:  Simon Wessel

    Args:
        FlaskForm (class): Class inherits from the FlaskForm class
    """
    user_name = StringField('Benutzername', validators=[InputRequired()])
    password = PasswordField('Passwort', validators=[InputRequired()])
    submit = SubmitField('Anmelden')

    def validate(self):     #Extends the validate-function
        """Custom validate function that tests for user existence and password correctness. 
        When data is invalid, add error messages that are rendered on the page. Author: Simon Wessel

        Returns:
            bool: True if user can be logged in, False if data is invalid
        """
        if not super(LoginForm, self).validate():
            return False
        user = User.query.filter_by(username=self.user_name.data).first()
        if not user:     # tests if username exists
            self.user_name.errors.append("Ungültige Login-Daten")
            return False
        if not user.check_password(self.password.data):     #Tests if password is correct
            self.password.errors.append('Ungültige Login-Daten')
            return False
        return True


class RegistrationForm(FlaskForm):
    """WTForm class for the registration form. Author:  Simon Wessel

    Args:
        FlaskForm (class): Class inherits from the FlaskForm class
    """
    user_name = StringField('Benutzername', validators=[InputRequired()])
    email = StringField(
        'E-Mail Addresse', validators=[Email(message="Bitte überprüfe die E-Mail-Adresse")])
    password = PasswordField('Passwort', [
        DataRequired(),
        EqualTo('confirm_password', message='Die Passwörter stimmen nicht überein')
    ])
    confirm_password = PasswordField('Passwort bestätigen', [InputRequired()])
    captcha = BooleanField('Ich bin kein Roboter', [InputRequired()])
    submit = SubmitField("Konto erstellen")

    def validate(self):
        """Custom validate function that tests the data contextually. When data is invalid, add error messages that are rendered on the page.
        Author: Simon Wessel

        Returns:
            bool: True if user can be create. False, when data is invalid.
        """
        if not super(RegistrationForm, self).validate():
            return False
        user = User.query.filter_by(username=self.user_name.data).first()
        if user:        #Tests, if the username is already assigned
            self.user_name.errors.append("Der Benutzername ist bereits vergeben")
            return False
        return True
        

class AccountSettings(FlaskForm):
    """WTForms class for the Account settings

    Args:
        FlaskForm (class): see above
    """
    user_name = StringField('Benutzername')
    email = StringField(
        'E-Mail Addresse', validators=[Email("Bitte überprüfe die E-Mail-Adresse")])
    new_password = PasswordField('Neues Passwort', [
        EqualTo('confirm_password', message='Die Passwörter stimmen nicht überein')
    ])
    confirm_password = PasswordField('Passwort bestätigen')
    submit = SubmitField("Änderungen speichern")

    def validate(self):
        """Custom validate function that tests the data contextually. When data is invalid, add error messages that are rendered on the page.
        Author: Simon Wessel

        Returns:
            bool: True if data can be written to db. False, when data is invalid.
        """
        if not super().validate():
            return False
        if self.user_name.data != current_user.username and User.query.filter_by(username=self.user_name.data).first():
            self.user_name.errors.append("Der Benutzername ist bereits vergeben.")
            return False
        return True