from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# In dieser Datei liegen die Datenbankklassen

class User(db.Model):
    __tablename__ = 'User'

    username = db.Column(db.String(45), primary_key=True)
    emailAdresse = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    rolle = db.Column(db.Integer(),  nullable=False)

    def __init__(self, username, emailAdresse, password, rolle) -> None:
        super().__init__()
        self.username = username
        self.emailAdresse = emailAdresse
        self.password = password
        self.rolle = rolle

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.username

    def __repr__(self):
        return f"<User {self.username}>"
