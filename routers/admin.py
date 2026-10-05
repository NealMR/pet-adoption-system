from fastapi import APIRouter, HTTPException
from models import StatusUpdate, Pet, AdoptionRequest
from routers.pets import pets_db
from routers.adoptions import adoptions_db

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.put("/pets/{pet_id}/status", response_model=Pet)
def update_pet_status(pet_id: str, status_update: StatusUpdate):
    """Update a pet's status (e.g., 'adopted', 'available')."""
    if pet_id not in pets_db:
        raise HTTPException(status_code=404, detail="Pet not found.")
    pets_db[pet_id].status = status_update.status
    return pets_db[pet_id]


@router.delete("/pets/{pet_id}")
def delete_pet(pet_id: str):
    """Remove a pet record from the database."""
    if pet_id not in pets_db:
        raise HTTPException(status_code=404, detail="Pet not found.")
    del pets_db[pet_id]
    return {"message": f"Pet '{pet_id}' has been removed successfully."}


@router.put("/adoptions/{request_id}/status", response_model=AdoptionRequest)
def update_adoption_request_status(request_id: str, status_update: StatusUpdate):
    """Approve or reject an adoption request. If approved, update pet status to 'adopted'."""
    if request_id not in adoptions_db:
        raise HTTPException(status_code=404, detail="Adoption request not found.")

    adoption_request = adoptions_db[request_id]
    adoption_request.status = status_update.status

    if status_update.status.lower() == "approved":
        pet_id = adoption_request.pet_id
        if pet_id in pets_db:
            pets_db[pet_id].status = "adopted"

    return adoption_request


@router.get("/dashboard")
def get_admin_dashboard():
    """Return dashboard summary: total pets, available pets, total requests, pending requests."""
    total_pets = len(pets_db)
    available_pets = sum(1 for pet in pets_db.values() if pet.status == "available")
    total_requests = len(adoptions_db)
    pending_requests = sum(1 for req in adoptions_db.values() if req.status == "pending")

    return {
        "total_pets": total_pets,
        "available_pets": available_pets,
        "total_requests": total_requests,
        "pending_requests": pending_requests,
    }
