from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Python CI/CD App", version="1.0.0")


class Item(BaseModel):
    name: str
    description: str = None
    price: float


@app.get("/health")
def health_check():
    """Health check endpoint for Kubernetes probes"""
    return {"status": "healthy"}


@app.get("/ready")
def readiness_check():
    """Readiness check endpoint for Kubernetes probes"""
    return {"status": "ready"}


@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Welcome to Python CI/CD Pipeline"}


@app.post("/items")
def create_item(item: Item):
    """Create a new item"""
    return {"item": item, "message": "Item created successfully"}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Get an item by ID"""
    return {"item_id": item_id, "name": f"Item {item_id}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
