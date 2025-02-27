# app/routers/items.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db  # Función para obtener la sesión de DB

router = APIRouter()

@router.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

@router.get("/items/", response_model=List[schemas.Item])
def get_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.get("/items/", response_model=List[schemas.Item])
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

