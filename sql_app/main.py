from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
        
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/games/new/", response_model=schemas.Game)
def create_game(db: Session = Depends(get_db)):
    # TODO: determine which user sent the request by JWT bearer
    db_user = crud.get_user_by_id(db, user_id)
    return crud.create_user_game(db=db, user_id=user_id)
    

@app.put("/games/invite/{invitee_id}/", response_model=schemas.Game)
def send_game_invite(
    user_id: int, game: schemas.Game, db: Session = Depends(get_db), invitee_id: int = None
):
    #TODO: pull the game from the db, then assert that it is not active, and update its status
    return crud.invite_to_game(db=db, game=game, invitee_id=invitee_id)


@app.put("/games/accept/{game_id}/", response_model=schemas.Game)
def accept_invite(
    user_id: int, game: schemas.Game, db: Session = Depends(get_db)
):
    return crud.accept_invite(db=db, game=game, user_id=user_id)


@app.get("/games/", response_model=List[schemas.Game])
def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    games = crud.get_games(db, skip=skip, limit=limit)
    return games
