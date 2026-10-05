from fastapi import FastAPI
from routers import pets, adoptions, admin

app = FastAPI(
    title="Pet Adoption & Management System",
    version="1.0.0"
)

app.include_router(pets.router)
app.include_router(adoptions.router)
app.include_router(admin.router)


@app.get("/")
def health_check():
    """Root endpoint for API health check."""
    return {"status": "ok", "message": "Pet Adoption API is running"}
