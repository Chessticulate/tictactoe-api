from typing import List
from typing_extensions import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi import FastAPI, Depends 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# do a scrappy migration to add the first users to the db
models.Base.metadata.create_all(bind=engine)

users = [
    models.User(id=idx, username=username, password="secret")
    for idx, username in enumerate(["brian", "kyle", "johnny", "stu", "taylor"])
]

session = SessionLocal()

for user in users: #TODO: add the list of users to the session instead of one at a time?
    session.add(user)
    session.commit()
    session.flush(user)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    return db.query(models.User).filter_by(username=token).first()


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return {"access_token": form_data.username, "token_type": "bearer"}


@app.get("/user/")
def get_user_id(user: Annotated[str, Depends(get_current_user)]):
    return user.id


@app.post("/games/new/", response_model=schemas.Game)
def create_game(db: Session = Depends(get_db), user_id: int = Depends(get_user_id)):
    return crud.create_game(db=db, user_id=user_id)
    

#@app.put("/games/invite/{invitee_id}/", response_model=schemas.Game)
#def send_game_invite(
#    user_id: int, game: schemas.Game, db: Session = Depends(get_db), invitee_id: int = None
#):
#    #TODO: pull the game from the db, then assert that it is not active, and update its status
#    return crud.invite_to_game(db=db, game=game, invitee_id=invitee_id)
#
#
#@app.put("/games/accept/{game_id}/", response_model=schemas.Game)
#def accept_invite(
#    user_id: int, game: schemas.Game, db: Session = Depends(get_db)
#):
#    return crud.accept_invite(db=db, game=game, user_id=user_id)
#
#
#@app.get("/games/", response_model=List[schemas.Game])
#def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#    games = crud.get_games(db, skip=skip, limit=limit)
#    return games
