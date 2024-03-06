from typing import Optional
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    __searchable__ = ['username']
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    accounts: so.WriteOnlyMapped['Account'] = so.relationship(back_populates='user')


    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
class Account(db.Model):
    account_no: so.Mapped[str] = so.mapped_column(sa.String(12),primary_key=True)
    balance: so.Mapped[str] = so.mapped_column()
    city: so.Mapped[str] = so.mapped_column(sa.String(40))
    mob_no: so.Mapped[str] = so.mapped_column(sa.String(10))
    pancard_no: so.Mapped[str] = so.mapped_column(sa.String(11))
    pincode: so.Mapped[str] = so.mapped_column(sa.String(6))
    creation_time: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    account_type : so.Mapped[str] = so.mapped_column(sa.String(40))
    username: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.username), index=True)

    user: so.Mapped[User] = so.relationship(back_populates='accounts')

    def __repr__(self):
        return '<Account {}>'.format(self.account_no)


@login.user_loader
def load_user(id):
    return db.session.get(User,int(id))

class Transaction(db.Model):

    id = sa.Column(sa.Integer, primary_key=True)
    sender_username = sa.Column(sa.String(64), sa.ForeignKey(User.username), nullable=False)
    receiver_username = sa.Column(sa.String(64), nullable=False)
    amount = sa.Column(sa.String, nullable=False)
    timestamp = sa.Column(sa.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.id}>'