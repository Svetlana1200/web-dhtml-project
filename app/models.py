from werkzeug import security
from flask_login import UserMixin
from app import db, lm


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = security.generate_password_hash(password)

    @classmethod
    def registrate(cls, login, password):
        user = cls(login=login)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
    
    def check_password(self, password):
        return security.check_password_hash(self.password_hash, password)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
