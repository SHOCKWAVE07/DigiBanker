from typing import Optional
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    accounts: so.WriteOnlyMapped['Account'] = so.relationship(back_populates='user')


    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Account(db.Model):
    account_no: so.Mapped[int] = so.mapped_column(primary_key=True)
    balance: so.Mapped[int] = so.mapped_column()
    city: so.Mapped[str] = so.mapped_column(sa.String(40))
    mob_no: so.Mapped[int] = so.mapped_column()
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    account_type : so.Mapped[str] = so.mapped_column(sa.String(40))
    username: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.username), index=True)

    user: so.Mapped[User] = so.relationship(back_populates='accounts')

    def __repr__(self):
        return '<Account {}>'.format(self.account_no)
