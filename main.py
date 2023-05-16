from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():     
    db = SessionLocal()     
    try:         
        yield db     
    finally:
         db.close()

@app.get('/user/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@app.post("/user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user.email)
    if db_user:
         raise HTTPException(
                  status_code=status.HTTP_400_BAD_REQUEST, 
                  detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/user/{user_id}/item/",  response_model=schemas.Item)
def create_item(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item, user_id)