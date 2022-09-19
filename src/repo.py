from sqlalchemy import and_
from src.db import session
import hashlib
from src.models import User, Contact, Phone, Email


def create_user(login, password):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    user = User(login=login, password=password)
    session.add(user)
    session.commit()


def create_contact(name, user):
    contact = Contact(name=name, user=user)
    session.add(contact)
    session.commit()


def create_phone(contact, phone):
    phone = Phone(phone_number=phone, contact=contact)
    session.add(phone)
    session.commit()


def create_email(contact, email):
    email = Email(email=email, contact=contact)
    session.add(email)
    session.commit()


def get_user(login) -> User:
    user = session.query(User).filter(User.login == login).one()
    return user


def get_contacts_by_user(user) -> list[Contact]:
    contacts = session.query(Contact).join(User).filter(Contact.user == user).all()
    return contacts


def get_contact(user, name) -> Contact:
    contact = session.query(Contact).filter(and_(Contact.user == user, Contact.name == name)).one()
    return contact

def get_phones_by_contact(contact) -> list[Phone]:
    phones = session.query(Phone).join(Contact).filter(Phone.contact_id == contact.id).all()
    return phones

def get_emails_by_contact(contact) -> list[Email]:
    emails = session.query(Email).join(Contact).filter(Email.contact_id == contact.id).all()
    return emails


def update_contact(name, new_name, user) -> bool:
    # print(name, new_name)
    contact = session.query(Contact).filter(and_(Contact.user == user, Contact.name == name))
    contact.update({'name': new_name})
    session.commit()
    session.close()
    return True


def remove_contact(_id, user) -> int:
    removing = session.query(Contact).filter(and_(Contact.user == user, Contact.id == _id)).delete()
    session.commit()
    session.close()
    return removing


def remove_phone(contact, phone):
    removing = session.query(Phone).filter(and_(contact.id == Phone.contact_id, Phone.phone_number == phone)).delete()
    session.commit()
    session.close()
    return removing


def remove_email(contact, email):
    removing = session.query(Email).filter(and_(contact.id == Email.contact_id, Email.email == email)).delete()
    session.commit()
    session.close()
    return removing
