from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, InputRequired
from .db import User


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
        # if user.password != self.password.data:     #Tests if password is correct
        if not user.check_password(self.password.data):     #Tests if password is correct
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
    confirm_password = PasswordField('Passwort bestätigen', [InputRequired()])
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
