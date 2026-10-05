from pydantic import BaseModel

class Pet(BaseModel):
    pet_id: str
    name: str
    species: str        # e.g., Dog, Cat, Rabbit
    breed: str
    age: int
    description: str
    status: str = "available"   # available | adopted

class AdoptionRequest(BaseModel):
    request_id: str
    pet_id: str
    adopter_name: str
    adopter_email: str
    message: str
    status: str = "pending"   # pending | approved | rejected

class StatusUpdate(BaseModel):
    status: str
