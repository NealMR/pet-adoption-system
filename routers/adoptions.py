"""
Adoption Request Router.
Handles adoption request submissions and retrievals backed by persistent database.
Author: Yash (S3_Yash)
"""
import collections.abc
from typing import Dict, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db, SessionLocal, init_db
from models import AdoptionRequest, AdoptionRequestModel, PetModel
from routers.pets import pets_db

router = APIRouter(prefix="/adoptions", tags=["Adoption Requests"])


# Database-backed dictionary proxy for backward compatibility with existing tests
class AdoptionDictProxy(collections.abc.MutableMapping):
    def __getitem__(self, key):
        init_db()
        with SessionLocal() as db:
            r = db.query(AdoptionRequestModel).filter(AdoptionRequestModel.request_id == key).first()
            if not r:
                raise KeyError(key)
            return r.to_dict()

    def __setitem__(self, key, val):
        init_db()
        with SessionLocal() as db:
            r = db.query(AdoptionRequestModel).filter(AdoptionRequestModel.request_id == key).first()
            if not r:
                data = {k: v for k, v in val.items() if k != "request_id"}
                r = AdoptionRequestModel(request_id=key, **data)
                db.add(r)
            else:
                for k, v in val.items():
                    if hasattr(r, k):
                        setattr(r, k, v)
            db.commit()

    def __delitem__(self, key):
        init_db()
        with SessionLocal() as db:
            r = db.query(AdoptionRequestModel).filter(AdoptionRequestModel.request_id == key).first()
            if not r:
                raise KeyError(key)
            db.delete(r)
            db.commit()

    def __iter__(self):
        init_db()
        with SessionLocal() as db:
            return iter([r.request_id for r in db.query(AdoptionRequestModel.request_id).all()])

    def __len__(self):
        init_db()
        with SessionLocal() as db:
            return db.query(AdoptionRequestModel).count()

    def __contains__(self, key):
        init_db()
        with SessionLocal() as db:
            return db.query(AdoptionRequestModel).filter(AdoptionRequestModel.request_id == key).first() is not None

    def clear(self):
        init_db()
        with SessionLocal() as db:
            db.query(AdoptionRequestModel).delete()
            db.commit()

    def values(self):
        init_db()
        with SessionLocal() as db:
            return [r.to_dict() for r in db.query(AdoptionRequestModel).all()]

    def pop(self, key, default=None):
        init_db()
        with SessionLocal() as db:
            r = db.query(AdoptionRequestModel).filter(AdoptionRequestModel.request_id == key).first()
            if not r:
                if default is not None:
                    return default
                raise KeyError(key)
            d = r.to_dict()
            db.delete(r)
            db.commit()
            return d


adoptions_db = AdoptionDictProxy()


@router.post("", response_model=dict)
@router.post("/", response_model=dict)
def submit_adoption_request(req: AdoptionRequest, db: Session = Depends(get_db)):
    """
    Submit a new adoption request in the persistent database.
    Validates duplicate request_id (400), target pet existence (404),
    and pet availability (400).
    """
    if db.query(AdoptionRequestModel).filter(AdoptionRequestModel.request_id == req.request_id).first():
        raise HTTPException(status_code=400, detail="Request ID exists")

    target_pet = db.query(PetModel).filter(PetModel.pet_id == req.pet_id).first()
    if not target_pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    if target_pet.status != "available":
        raise HTTPException(status_code=400, detail="Pet not available")

    new_req = AdoptionRequestModel(
        request_id=req.request_id,
        pet_id=req.pet_id,
        adopter_name=req.adopter_name,
        adopter_email=req.adopter_email,
        message=req.message,
        status=req.status or "pending"
    )
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return {"message": "Request submitted", "data": new_req.to_dict()}


@router.get("", response_model=List[dict])
@router.get("/", response_model=List[dict])
def get_requests(db: Session = Depends(get_db)):
    """
    Retrieve all adoption requests from persistent database.
    """
    requests = db.query(AdoptionRequestModel).all()
    return [r.to_dict() for r in requests]


@router.get("/my-requests")
@router.get("/my-requests/")
def get_my_requests(email: str, db: Session = Depends(get_db)):
    """
    Retrieve adoption requests by adopter email.
    """
    requests = db.query(AdoptionRequestModel).filter(AdoptionRequestModel.adopter_email == email).all()
    return [r.to_dict() for r in requests]


@router.get("/{request_id}")
def get_request(request_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific adoption request by ID.
    Returns 404 if not found.
    """
    req = db.query(AdoptionRequestModel).filter(AdoptionRequestModel.request_id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return req.to_dict()

