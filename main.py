from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(
    title="FastAPI Aplikace",
    description="Jednoduchá FastAPI aplikace",
    version="1.0.0"
)

# Přidání CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # V produkci použijte konkrétní domény
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic modely
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

# In-memory úložiště pro demo
items_db = []
next_id = 1

@app.get("/")
async def root():
    """Základní endpoint"""
    return {"message": "FastAPI aplikace běží!", "status": "OK"}

@app.get("/health")
async def health_check():
    """Health check endpoint pro Docker"""
    return {"status": "healthy", "service": "fastapi"}

@app.get("/items", response_model=List[ItemResponse])
async def get_items():
    """Získat všechny položky"""
    return items_db

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """Získat položku podle ID"""
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Položka nenalezena")

@app.post("/items", response_model=ItemResponse)
async def create_item(item: Item):
    """Vytvořit novou položku"""
    global next_id
    new_item = ItemResponse(
        id=next_id,
        name=item.name,
        description=item.description,
        price=item.price
    )
    items_db.append(new_item)
    next_id += 1
    return new_item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)