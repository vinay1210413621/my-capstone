from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

app = FastAPI(
    title="Inventory Management System",
    version="1.0.0"
)


# -----------------------------
# Data Model
# -----------------------------

class Item(BaseModel):
    name: str
    sku: str
    quantity: int
    category: str = "General"


# -----------------------------
# In-memory database
# -----------------------------

items = []


# -----------------------------
# Frontend
# -----------------------------

@app.get("/")
def serve_frontend():
    return FileResponse(Path(__file__).parent / "index.html")


# -----------------------------
# Health checks
# -----------------------------

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/ready")
def readiness_check():
    return {"status": "ready"}


# -----------------------------
# Inventory APIs
# -----------------------------

@app.get("/items")
def get_items():
    return items


@app.post("/items")
def create_item(item: Item):

    new_item = {
        "id": str(len(items) + 1),
        "name": item.name,
        "sku": item.sku,
        "quantity": item.quantity,
        "category": item.category
    }

    items.append(new_item)

    return new_item


@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item):

    for existing_item in items:

        if existing_item["id"] == item_id:

            existing_item["name"] = item.name
            existing_item["sku"] = item.sku
            existing_item["quantity"] = item.quantity
            existing_item["category"] = item.category

            return existing_item

    raise HTTPException(
        status_code=404,
        detail="Item not found"
    )


@app.delete("/items/{item_id}")
def delete_item(item_id: str):

    for index, item in enumerate(items):

        if item["id"] == item_id:

            deleted_item = items.pop(index)

            return {
                "message": "Item deleted successfully",
                "item": deleted_item
            }

    raise HTTPException(
        status_code=404,
        detail="Item not found"
    )


# -----------------------------
# Run application
# -----------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )