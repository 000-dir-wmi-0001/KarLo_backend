from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import contribute_schema
from app.services.contribute import contribute_service
from app.db.session import get_db

contribute_router = APIRouter(prefix="/contribute", tags=["Contribute"])

@contribute_router.post(
    "/create",
    response_model=contribute_schema.CreateContributeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_contribute(
    contribute: contribute_schema.ContributeCreate,
    db: Session = Depends(get_db)
):
    new_contribution = contribute_service.create_contribution(contribute, db)
    return {
        "data": new_contribution,
        "message": "Contribution created successfully"
    }

@contribute_router.get("/{id}", response_model=contribute_schema.ContributeResponse)
def get_contribute(id: int, db: Session = Depends(get_db)):
    result = contribute_service.get_contribution_by_id(id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Contribution not found")
    return result

@contribute_router.get("/", response_model=contribute_schema.ContributeListResponse)
def get_all_contributes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contributions = contribute_service.get_all_contributions(db, skip, limit)
    return {
        "contributions": contributions,
        "total": len(contributions)
    }

@contribute_router.put("/update/{id}", response_model=contribute_schema.ContributeResponse)
def update_contribute(
    id: int,
    contribute: contribute_schema.ContributeUpdate,
    db: Session = Depends(get_db)
):
    result = contribute_service.update_contribution(id, contribute, db)
    if not result:
        raise HTTPException(status_code=404, detail="Contribution not found")
    return result

@contribute_router.delete("/delete/{id}", response_model=contribute_schema.ContributeDeleteResponse)
def delete_contribute(id: int, db: Session = Depends(get_db)):
    result = contribute_service.delete_contribution(id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Contribution not found")
    return {
        "success": True,
        "message": f"Contribution with ID {id} deleted successfully"
    }

@contribute_router.get("/email/{email}", response_model=contribute_schema.ContributeResponse)
def get_contribution_by_email(email: str, db: Session = Depends(get_db)):
    result = contribute_service.get_contribution_by_email(email, db)
    if not result:
        raise HTTPException(status_code=404, detail="Contribution not found")
    return result

@contribute_router.get("/country/{country}", response_model=list[contribute_schema.ContributeResponse])
def get_contributions_by_country(country: str, db: Session = Depends(get_db)):
    result = contribute_service.get_contributions_by_country(country, db)
    if not result:
        raise HTTPException(status_code=404, detail="No contributions found for this country")
    return result
