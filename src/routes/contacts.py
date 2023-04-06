# Роутер(маршрут) для модуля contacts - містить точки доступу для операцій CRUD
from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi_pagination import Page, add_pagination  # , paginate  # poetry add fastapi-pagination
# from fastapi_pagination.ext.async_sqlmodel import paginate
from sqlalchemy.orm import Session

from src.database.db_connect import get_db
from src.database.models import Contact, User
from src.repository import contacts as repository_contacts
from src.schemes import ContactModel, ContactResponse, CatToNameModel
from src.services.auth import auth_service


router = APIRouter(prefix='/contacts')  # tags=["contacts"]


# response_model=List[ContactResponse]   # limit: int = Query(10, le=500), offset: int = 0,
@router.get("/", response_model=Page[ContactResponse], tags=['all_contacts'])
async def get_contacts(db: Session = Depends(get_db), 
                       current_user: User = Depends(auth_service.get_current_user)
                       ) -> Optional[Page[ContactResponse]]:
    contacts = await repository_contacts.get_contacts(db)  # limit, offset, 

    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, tags=['contact'])
async def get_contact(contact_id: int = Path(ge=1),
                      db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)
                      ) -> Union[Contact, HTTPException]:
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.post("/", response_model=ContactResponse,  status_code=status.HTTP_201_CREATED, tags=['contact'])
async def create_contact(body: ContactModel,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)
                         ) -> Optional[Contact]:

    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse, tags=['contact'])
async def update_contact(body: ContactModel,
                         contact_id: int = Path(ge=1),  # =Path(ge=1) ?
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)
                         ) -> Union[Contact, HTTPException]:  
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")

    return contact


# response_model=ContactResponse or status_code=status.HTTP_204_NO_CONTENT ? ...
@router.delete("/{contact_id}", response_model=ContactResponse, tags=['contact'])
async def remove_contact(contact_id: int = Path(ge=1),
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)
                         ) -> Union[Contact, HTTPException]:
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.patch("/{contact_id}/to_name", response_model=ContactResponse, tags=['contact'])
async def change_name_contact(body: CatToNameModel,
                              contact_id: int = Path(ge=1),
                              db: Session = Depends(get_db),
                              current_user: User = Depends(auth_service.get_current_user)
                              ) -> Union[Contact, HTTPException]:
    contact = await repository_contacts.change_name_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    return contact


@router.get("/search_by_name/{name}", response_model=ContactResponse, tags=['search'])
async def search_by_name(name: str,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)
                         ) -> Union[Contact, HTTPException]:
    contact = await repository_contacts.search_by_name(name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_last_name/{last_name}", response_model=ContactResponse, tags=['search'])
async def search_by_last_name(last_name: str,
                              db: Session = Depends(get_db),
                              current_user: User = Depends(auth_service.get_current_user)
                              ) -> Union[Contact, HTTPException]:
    contact = await repository_contacts.search_by_last_name(last_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_email/{email}", response_model=ContactResponse, tags=['search'])
async def search_by_email(email: str,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)
                          ) -> Union[Contact, HTTPException]:
    contact = await repository_contacts.search_by_email(email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_phone/{phone}", response_model=ContactResponse, tags=['search'])
async def search_by_phone(phone: int,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)
                          ) -> Union[Contact, HTTPException]:
    contact = await repository_contacts.search_by_phone(phone, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_birthday_celebration_within_days/{days}", response_model=Page[ContactResponse], tags=['search'])
async def search_by_birthday_celebration_within_days(days: int,
                                                     db: Session = Depends(get_db),
                                                     current_user: User = Depends(auth_service.get_current_user)
                                                     ) -> Union[Page[ContactResponse], HTTPException]:
    contact = await repository_contacts.search_by_birthday_celebration_within_days(days, db)
    if contact is None:  # NoConnection in database...
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact  # paginate(contact)


@router.get("/search_by_like_name/{name}", response_model=Page[ContactResponse], tags=['search'])
async def search_by_like_name(name: str,
                              db: Session = Depends(get_db),
                              current_user: User = Depends(auth_service.get_current_user)
                              ) -> Union[Page[ContactResponse], HTTPException]:
    contact = await repository_contacts.search_by_like_name(name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_like_last_name/{last_name}", response_model=Page[ContactResponse], tags=['search'])
async def search_by_like_last_name(last_name: str,
                                   db: Session = Depends(get_db),
                                   current_user: User = Depends(auth_service.get_current_user)
                                   ) -> Union[Page[ContactResponse], HTTPException]:
    contact = await repository_contacts.search_by_like_last_name(last_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_like_email/{email}", response_model=Page[ContactResponse], tags=['search'])
async def search_by_like_email(email: str,
                               db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)
                               ) -> Union[Page[ContactResponse], HTTPException]:
    contact = await repository_contacts.search_by_like_email(email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


@router.get("/search_by_like_phone/{phone}", response_model=Page[ContactResponse], tags=['search'])
async def search_by_like_phone(phone: int,
                               db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)
                               ) -> Union[Page[ContactResponse], HTTPException]:
    contact = await repository_contacts.search_by_like_phone(phone, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found")
    
    return contact


add_pagination(router)
