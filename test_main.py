import pytest
from fastapi.testclient import TestClient
from main import app
from routers.pets import pets_db
from routers.adoptions import adoptions_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    """Clear in-memory databases before each test."""
    pets_db.clear()
    adoptions_db.clear()
    yield
    pets_db.clear()
    adoptions_db.clear()


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Pet Adoption API is running"}


def test_update_pet_status():
    # Setup pet
    pet_data = {
        "pet_id": "pet1",
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "description": "Friendly dog",
        "status": "available"
    }
    client.post("/pets/", json=pet_data)

    # Update status
    response = client.put("/admin/pets/pet1/status", json={"status": "adopted"})
    assert response.status_code == 200
    assert response.json()["status"] == "adopted"
    assert pets_db["pet1"].status == "adopted"


def test_update_pet_status_not_found():
    response = client.put("/admin/pets/nonexistent/status", json={"status": "adopted"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Pet not found."


def test_delete_pet():
    # Setup pet
    pet_data = {
        "pet_id": "pet2",
        "name": "Milo",
        "species": "Cat",
        "breed": "Siamese",
        "age": 2,
        "description": "Playful cat",
        "status": "available"
    }
    client.post("/pets/", json=pet_data)

    # Delete pet
    response = client.delete("/admin/pets/pet2")
    assert response.status_code == 200
    assert "removed successfully" in response.json()["message"]
    assert "pet2" not in pets_db


def test_delete_pet_not_found():
    response = client.delete("/admin/pets/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Pet not found."


def test_approve_adoption_request():
    # Setup pet and request
    pet_data = {
        "pet_id": "pet3",
        "name": "Luna",
        "species": "Rabbit",
        "breed": "Dutch",
        "age": 1,
        "description": "Cute bunny",
        "status": "available"
    }
    client.post("/pets/", json=pet_data)

    request_data = {
        "request_id": "req1",
        "pet_id": "pet3",
        "adopter_name": "Alice",
        "adopter_email": "alice@example.com",
        "message": "I love bunnies"
    }
    client.post("/adoptions/", json=request_data)

    # Approve adoption request
    response = client.put("/admin/adoptions/req1/status", json={"status": "approved"})
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
    assert adoptions_db["req1"].status == "approved"
    assert pets_db["pet3"].status == "adopted"


def test_reject_adoption_request():
    # Setup pet and request
    pet_data = {
        "pet_id": "pet4",
        "name": "Charlie",
        "species": "Dog",
        "breed": "Poodle",
        "age": 4,
        "description": "Smart dog",
        "status": "available"
    }
    client.post("/pets/", json=pet_data)

    request_data = {
        "request_id": "req2",
        "pet_id": "pet4",
        "adopter_name": "Bob",
        "adopter_email": "bob@example.com",
        "message": "Interested in Charlie"
    }
    client.post("/adoptions/", json=request_data)

    # Reject adoption request
    response = client.put("/admin/adoptions/req2/status", json={"status": "rejected"})
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"
    assert adoptions_db["req2"].status == "rejected"
    assert pets_db["pet4"].status == "available"  # Status remains available if rejected


def test_update_adoption_request_not_found():
    response = client.put("/admin/adoptions/nonexistent/status", json={"status": "approved"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Adoption request not found."


def test_admin_dashboard():
    # Setup pets
    client.post("/pets/", json={
        "pet_id": "pet1", "name": "P1", "species": "Dog", "breed": "B1", "age": 1, "description": "D1", "status": "available"
    })
    client.post("/pets/", json={
        "pet_id": "pet2", "name": "P2", "species": "Cat", "breed": "B2", "age": 2, "description": "D2", "status": "available"
    })

    # Setup adoptions
    client.post("/adoptions/", json={
        "request_id": "req1", "pet_id": "pet1", "adopter_name": "A1", "adopter_email": "a1@test.com", "message": "M1"
    })

    dashboard_res = client.get("/admin/dashboard")
    assert dashboard_res.status_code == 200
    data = dashboard_res.json()
    assert data["total_pets"] == 2
    assert data["available_pets"] == 2
    assert data["total_requests"] == 1
    assert data["pending_requests"] == 1

    # Approve request
    client.put("/admin/adoptions/req1/status", json={"status": "approved"})

    dashboard_res2 = client.get("/admin/dashboard")
    assert dashboard_res2.status_code == 200
    data2 = dashboard_res2.json()
    assert data2["total_pets"] == 2
    assert data2["available_pets"] == 1
    assert data2["total_requests"] == 1
    assert data2["pending_requests"] == 0
