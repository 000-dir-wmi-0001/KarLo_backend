from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.home_cure.schemas import contact_schema
from app.home_cure.services import contact_service
from app.db.session import get_db
from app.utils.mail.dispatchEmail import dispatch
from app.core.config import settings

contact_router = APIRouter(prefix="/contact", tags=["Contact"])

@contact_router.post(
    "/create",
    response_model=contact_schema.CreateContactResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_contact(
    contact: contact_schema.ContactCreate,
    db: Session = Depends(get_db)
):
    new_contact = contact_service.create_contact(contact, db)
    # Send notification email (non-blocking failures are okay)
    try:
        await dispatch(
            "contact",
            [settings.EMAIL_ADMIN],
            {
                "name": contact.name,
                "email": contact.email,
                "message": contact.message,
                "subject": contact.subject,
            },
        )
    except Exception:
        # Silently ignore email errors to not block API success
        pass
    return {
        "data": new_contact,
        "message": "Contact created successfully"
    }

@contact_router.get("/{id}", response_model=contact_schema.ContactResponse)
def get_contact(id: int, db: Session = Depends(get_db)):
    result = contact_service.get_contact_by_id(id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Contact not found")
    return result

@contact_router.get("/", response_model=contact_schema.ContactListResponse)
def get_all_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = contact_service.get_all_contacts(db, skip, limit)
    return {
        "contacts": contacts,
        "total": len(contacts)
    }

@contact_router.put("/update/{id}", response_model=contact_schema.ContactResponse)
def update_contact(
    id: int,
    contact: contact_schema.ContactUpdate,
    db: Session = Depends(get_db)
):
    result = contact_service.update_contact(id, contact, db)
    if not result:
        raise HTTPException(status_code=404, detail="Contact not found")
    return result

@contact_router.delete("/delete/{id}", response_model=contact_schema.ContactDeleteResponse)
def delete_contact(id: int, db: Session = Depends(get_db)):
    result = contact_service.delete_contact(id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {
        "success": True,
        "message": f"Contact with ID {id} deleted successfully"
    }

@contact_router.get("/email/{email}", response_model=contact_schema.ContactResponse)
def get_contact_by_email(email: str, db: Session = Depends(get_db)):
    result = contact_service.get_contact_by_email(email, db)
    if not result:
        raise HTTPException(status_code=404, detail="Contact not found")
    return result

