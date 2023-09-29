from sqlalchemy.orm import Session

from . import models, schemas


def create_game(db: Session, user_id: int):
    db_game = models.Game(owner_id=user_id, state="---------")
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def invite_to_game(db: Session, game: schemas.Game, invite_id: int):
    pass


def accept_invite(db: Session, game: schemas.Game, invitee_id: int):
    pass


def move(db: Session, game_id: int, move: str):
    pass
