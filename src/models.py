from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=datetime.now())


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    user = relationship(User)


class Phone(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), nullable=False, unique=True)
    created = Column(DateTime, default=datetime.now())
    contact_id = Column(Integer, ForeignKey('contacts.id', ondelete="CASCADE"))
    contact = relationship(Contact)


class Email(Base):
    __tablename__ = 'emails'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    created = Column(DateTime, default=datetime.now())
    contact_id = Column(Integer, ForeignKey('contacts.id', ondelete="CASCADE"))
    contact = relationship(Contact)
