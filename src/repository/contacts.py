# функції для взаємодії з базою даних.
from datetime import date, timedelta
from typing import Optional

from fastapi import HTTPException, status
from fastapi_pagination import Page  # , paginate  # poetry add fastapi-pagination
from fastapi_pagination.ext.sqlalchemy import paginate
# from fastapi_pagination.ext.sqlmodel import paginate
from sqlalchemy import cast, func, String
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemes import ContactModel, CatToNameModel, ContactResponse


async def get_contacts(user: User, 
                       db: Session) -> Optional[Page[ContactResponse]]:
    """To retrieve a list of records from a database with the ability to skip 
    a certain number of records and limit the number returned."""
    # return db.query(Contact).limit(limit).offset(offset).all()
    return paginate(db.query(Contact).filter(Contact.user_id == user.id).order_by(Contact.name))


async def get_contact(contact_id: int, 
                      user: User,
                      db: Session) -> Optional[Contact]:
    """To get a particular record by its ID."""
    # return db.query(Contact).filter(Contact.id == contact_id).first()
    return db.query(Contact).filter(Contact.user_id == user.id).filter_by(id=contact_id).first()  


async def create_contact(body: ContactModel, 
                         user: User,
                         db: Session) -> Optional[Contact]:
    """Creating a new record in the database. Takes a ContactModel object and uses the information 
    from it to create a new Contact object, then adds it to the session and 
    commits the changes to the database."""
    contact = (db.query(Contact).filter(Contact.user_id == user.id).filter_by(email=body.email).first() or
               db.query(Contact).filter(Contact.user_id == user.id).filter_by(phone=body.phone).first() or
               db.query(Contact).filter(Contact.user_id == user.id).filter_by(name=body.name, 
                                                                              last_name=body.last_name).first())
    if contact:  # raise формує свою відповідь взамін return (все що після - відміняється):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Duplicate data')
    
    contact = Contact(**body.dict(), user_id=user.id)  # !!!!!!!!!!!! , user_id=user.id  or , user=user
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int,
                         body: ContactModel,
                         user: User,
                         db: Session) -> Optional[Contact]:
    """Update a specific record by its ID. Takes the ContactModel object and updates the information from it 
    by the name of the record. If the record does not exist - None is returned."""
    # contact = db.query(Contact).filter(contact.id == contact_id).first()
    contact = db.query(Contact).filter(Contact.user_id == user.id).filter_by(id=contact_id).first()
    if contact:
        contact.name = body.name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.description = body.description
        db.commit()
    return contact


async def remove_contact(contact_id: int,
                         user: User,
                         db: Session) -> Optional[Contact]:
    """Delete a specific record by its ID. If the record does not exist - None is returned."""
    # contact = db.query(Contact).filter(Contact.id == contact_id).first()
    contact = db.query(Contact).filter(Contact.user_id == user.id).filter_by(id=contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def change_name_contact(body: CatToNameModel,
                              contact_id: int,
                              user: User,
                              db: Session) -> Optional[Contact]:
    """To update only the name of the record."""
    contact = db.query(Contact).filter(Contact.user_id == user.id).filter_by(id=contact_id).first()
    if contact:
        contact.name = body.name
        db.commit()
    return contact


async def search_by_name(name: str,
                         user: User,
                         db: Session) -> Optional[Contact]:
    """To search for a record by a specific name."""
    # return db.query(Contact).filter(Contact.name == name).first()  # .all()
    return db.query(Contact).filter(Contact.user_id == user.id).filter_by(name=name).first()


async def search_by_last_name(last_name: str,
                              user: User,
                              db: Session) -> Optional[Contact]:
    """To search for a record by a specific last name."""
    # return db.query(Contact).filter(Contact.last_name == last_name).first()
    return db.query(Contact).filter(Contact.user_id == user.id).filter_by(last_name=last_name).first() 


async def search_by_email(email: str,
                          user: User,
                          db: Session) -> Optional[Contact]:
    """To search for a record by a certain email."""
    # return db.query(Contact).filter(Contact.email == email).first()
    return db.query(Contact).filter(Contact.user_id == user.id).filter_by(email=email).first()


async def search_by_phone(phone: int,
                          user: User,
                          db: Session) -> Optional[Contact]:
    """To search for a record by a certain phone."""
    # return db.query(Contact).filter(Contact.phone == phone).first()
    return db.query(Contact).filter(Contact.user_id == user.id).filter_by(phone=phone).first()


# https://stackoverflow.com/questions/4926757/sqlalchemy-query-where-a-column-contains-a-substring
async def search_by_like_name(part_name: str,
                              user: User,
                              db: Session) -> Optional[Page[ContactResponse]]:
    """To search for an entry by a partial match in the name."""
    return paginate(db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.name.icontains(part_name)))  # if default .all()


async def search_by_like_last_name(part_last_name: str,
                                   user: User,
                                   db: Session) -> Optional[Page[ContactResponse]]:
    """To search for a record by a partial match in the last name."""
    return paginate(db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.last_name.icontains(part_last_name))) 


async def search_by_like_email(part_email: str,
                               user: User,
                               db: Session) -> Optional[Page[ContactResponse]]:
    """To search for a record by a partial match in an email."""
    return paginate(db.query(Contact).filter(Contact.user_id == user.id).filter(Contact.email.icontains(part_email)))


# https://stackoverflow.com/questions/23622993/postgresql-error-operator-does-not-exist-integer-character-varying
# https://stackoverflow.com/questions/33946865/flask-sqlalchemy-postgresql-in-a-query-can-an-int-be-cast-to-a-string
async def search_by_like_phone(part_phone: int,
                               user: User,
                               db: Session) -> Optional[Page[ContactResponse]]:
    """To search for a record by a partial match in phone."""
    return paginate(db.query(Contact).filter(Contact.user_id == user.id).filter(cast(Contact.phone, String).icontains(str(part_phone))))


# https://github.com/uriyyo/fastapi-pagination
# https://uriyyo-fastapi-pagination.netlify.app/
# https://stackoverflow.com/questions/16589208/attributeerror-while-querying-neither-instrumentedattribute-object-nor-compa
async def search_by_birthday_celebration_within_days(meantime: int,   # Optional[List[Type[Contact]]]
                                                     user: User,
                                                     db: Session) -> Optional[Page[ContactResponse]]: 
    """To find contacts celebrating birthdays in the next (meantime) days."""
    today = date.today()
    days_limit = date.today() + timedelta(meantime)
    slide = 1 if days_limit.year - today.year else 0

    # func.to_date(Contact.birthday.year, 'YYYY-MM-DD')
    # func.to_char(Contact.birthday, 'MM-DD')
    # https://stackoverflow.com/questions/12069236/sqlalchemy-select-to-date
    # https://stackoverflow.com/questions/17333014/convert-selected-datetime-to-date-in-sqlalchemy
    return paginate(db.query(Contact).filter(Contact.user_id == user.id).filter(func.to_char(Contact.birthday,
                                                          f'{slide}MM-DD') >= today.strftime(f"0%m-%d"),
                                             func.to_char(Contact.birthday,
                                                          '0MM-DD') <= days_limit.strftime(f"{slide}%m-%d")))
