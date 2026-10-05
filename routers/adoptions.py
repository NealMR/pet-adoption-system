from fastapi import APIRouter, HTTPException
from typing import List

from models import AdoptionRequest, StatusUpdate
from routers.pets import pets_db

router = APIRouter(prefix="/adoptions", tags=["Adoption Requests"])

# In-memory store for adoption requests
adoptions_db = {}


@router.post("/", response_model=AdoptionRequest)
def submit_adoption_request(request: AdoptionRequest):
    """Submit a new adoption request for an available pet."""
    # Check that the pet exists
    if request.pet_id not in pets_db:
        raise HTTPException(status_code=404, detail="Pet not found.")

    # Check that the pet is available
    pet = pets_db[request.pet_id]
    if pet.status != "available":
        raise HTTPException(
            status_code=400,
            detail=f"Pet '{request.pet_id}' is not available for adoption (current status: {pet.status})."
        )

    # Check for duplicate request_id
    if request.request_id in adoptions_db:
        raise HTTPException(
            status_code=400,
            detail="An adoption request with this ID already exists."
        )

    adoptions_db[request.request_id] = request
    return request


@router.get("/", response_model=List[AdoptionRequest])
def get_all_adoption_requests():
    """Retrieve all adoption requests."""
    return list(adoptions_db.values())


@router.get("/{request_id}", response_model=AdoptionRequest)
def get_adoption_request(request_id: str):
    """Retrieve a specific adoption request by ID."""
    if request_id not in adoptions_db:
        raise HTTPException(status_code=404, detail="Adoption request not found.")
    return adoptions_db[request_id]
