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


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return {"access_token": form_data.username, "token_type": "bearer"}


@app.get("/user/")
def get_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    return db.query(models.User).filter_by(username=token).first()


@app.post("/games/new/", response_model=schemas.Game)
def create_game(db: Session = Depends(get_db), owner: models.User = Depends(get_user)):
    return crud.create_game(db=db, owner_id=owner.id)


@app.get("/games/", response_model=List[schemas.Game])
def read_games(db: Session = Depends(get_db)):
    return crud.get_games(db)


@app.put("/invite/{invitee_id}/", response_model=schemas.Game)
def invite(invitee_id: int, db: Session = Depends(get_db), owner: models.User = Depends(get_user)):
    game = owner.owned_games[0]
    return crud.invite(invitee_id=invitee_id, db=db, game=game)


@app.put("/accept/{game_id}", response_model=schemas.Game)
def accept(game_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_user)):
    game = crud.get_game(db=db, game_id=game_id)
    return crud.accept(invitee_id=user.id, db=db, game=game)


@app.put("/move/{game_id}/{move}", response_model=schemas.Game)
def move(game_id: int, move: int, db: Session = Depends(get_db), user: models.User = Depends(get_user)):
    game = crud.get_game(db=db, game_id=game_id)
    crud.move(db=db, game=game, user=user, move=move)
    return crud.step_player(db=db, game=game, user=user)
