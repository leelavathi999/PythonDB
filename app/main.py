from fastapi import FastAPI

from app.api.routers import users,items
app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(items.router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "FastAPI Connection with Postgrasql"}
