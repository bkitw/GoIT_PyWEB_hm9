import argparse
import sys
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.repo import get_user, create_contact, get_contacts_by_user, update_contact, \
    remove_contact, create_user, create_phone, get_contact, create_email, remove_phone, remove_email, \
    get_phones_by_contact, get_emails_by_contact
import hashlib

parser = argparse.ArgumentParser(description='Personal assistant APP')
parser.add_argument('--action', help='Commands: create_contact, create_phone, create_email,\n'
                                     'get_user, get_contacts_by_user, get_phones_by_contact, get_emails_by_contact,\n'
                                     'update_contact,\n'
                                     'remove_contact, remove_phone, remove_email.')
parser.add_argument('--id', help='Value of primary key of the contact.')
parser.add_argument('--name', help='Value of "name"-field in the table "Contacts".')
parser.add_argument('--login', help='Value of "login"-field in the table "Users".')
parser.add_argument('--new_name', help='Value of "name"-field of specifically contact that you want to insert '
                                       'instead of old one.')
parser.add_argument('--phone', help='Value of "phone_number"-field in the table "Phones".')
parser.add_argument('--email', help='Value of "email"-field in the table "Emails".')

arguments = parser.parse_args()
my_arg = vars(arguments)

action = my_arg.get('action')
name = my_arg.get('name')
_id = my_arg.get('id')
login = my_arg.get('login')
new_name = my_arg.get('new_name')
phone = my_arg.get('phone')
email = my_arg.get('email')


def main(user):
    global phone, email
    match action:
        case 'create':
            create_contact(name=name, user=user)
            print(f'Contact "{name}" created!')
        case 'list':
            contacts = get_contacts_by_user(user)
            for contact in contacts:
                print(contact.name, contact.user.login)
        case 'update':
            contact = update_contact(name=name, new_name=new_name, user=user)
            print(contact)
        case 'remove':
            r = remove_contact(_id=_id, user=user)
            print(f'Result: {bool(r)}')
        case 'remove_phone':
            contact = get_contact(user=user, name=name)
            r = remove_phone(contact=contact, phone=phone)
            if r:
                print(f'Result: {bool(r)}')
            else:
                print('Guess you trying to delete an non-existing number!')
        case 'remove_email':
            contact = get_contact(user=user, name=name)
            r = remove_email(contact=contact, email=email)
            if r:
                print(f'Result: {bool(r)}')
            else:
                print('Guess you trying to delete an non-existing email!')
        case 'create_phone':
            try:
                contact = get_contact(user=user, name=name)
            except SQLAlchemyError:
                print('Oops! Something gone wrong.')
                sys.exit()
            try:
                create_phone(contact=contact, phone=phone)
                print(f'Phone number for {contact.name} created!')
            except IntegrityError:
                print('Guess, this number already exists!')
        case 'create_email':
            try:
                contact = get_contact(user=user, name=name)
            except SQLAlchemyError:
                print('Oops! Something gone wrong.')
                sys.exit()
            try:
                create_email(contact=contact, email=email)
                print(f'Email for {contact.name} created!')
            except IntegrityError:
                print('Guess, this mail already exists!')
        case 'get_phones_by_contact':
            contact = get_contact(user=user, name=name)
            phones = get_phones_by_contact(contact=contact)
            for phone in phones:
                print(phone.phone_number + " belongs to -- " + phone.contact.name)
        case 'get_emails_by_contact':
            contact = get_contact(user=user, name=name)
            emails = get_emails_by_contact(contact=contact)
            for email in emails:
                print(email.email + " belongs to -- " + email.contact.name)


if __name__ == '__main__':
    try:
        user = get_user(login)
        password = hashlib.md5(input('password: ').encode('utf-8')).hexdigest()
        if password == user.password:
            try:
                main(user)
            except SQLAlchemyError as err:
                print(err)
        else:
            print('Wrong password!')
            sys.exit()
    except SQLAlchemyError as fuck:
        print('This user does not exists!\nWould you like to create a new one?')
        password = input('Create your password --> ')
        create_user(login, password)
        print(f'New user with nickname {login} created!')
        sys.exit()
