from fastapi import APIRouter, HTTPException
from models import Pet
from typing import List

router = APIRouter(prefix="/pets", tags=["Pet Management"])

pets_db = {}

@router.post("/", response_model=Pet)
def register_pet(pet: Pet):
    if pet.pet_id in pets_db:
        raise HTTPException(status_code=400, detail="Pet with this ID already exists.")
    pets_db[pet.pet_id] = pet
    return pet

@router.get("/", response_model=List[Pet])
def get_all_pets():
    return list(pets_db.values())

@router.get("/{pet_id}", response_model=Pet)
def get_pet(pet_id: str):
    if pet_id not in pets_db:
        raise HTTPException(status_code=404, detail="Pet not found.")
    return pets_db[pet_id]
