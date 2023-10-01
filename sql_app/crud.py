from sqlalchemy.orm import Session

from . import models, schemas


def create_game(db: Session, owner_id: int):
    db_game = models.Game(owner_id=owner_id, state="---------")
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def invite(db: Session, game: int, invitee_id: int):
    invitee = db.query(models.User).filter_by(id=invitee_id).first()
    game.invitee = invitee
    db.commit()
    return game


def get_game(db: Session, game_id: int):
    return db.query(models.Game).filter_by(id=game_id).first()


def accept(invitee_id: int, db: Session, game: schemas.Game):
    game.next_player_id = game.owner.id
    db.commit()
    return game


def move(db: Session, game: schemas.Game, user: schemas.User, move: int):
    symbol = "X" if game.owner_id == user.id else "O"
    temp = list(game.state)
    temp[move] = symbol
    game.state = "".join(temp)
    db.commit()
    return game


def step_player(db: Session, game: models.Game, user: models.User):
    next_player_id = game.owner_id if game.owner_id != user.id else game.invitee_id
    game.next_player_id = next_player_id
    db.commit()
    return game


def get_games(db: Session):
    return db.query(models.Game).all()
