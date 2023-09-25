from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column

from .database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(String, index=True)

    owner_id = Column(Integer, ForeignKey("users.id"))
    invitee_id = mapped_column(ForeignKey("users.id"))

    owner = relationship("User", back_populates="owned_games", foreign_keys=[owner_id])
    invitee = relationship("User", back_populates="invited_games", foreign_keys=[invitee_id])


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)

    owned_games = relationship("Game", back_populates="owner", primaryjoin=id==Game.owner_id)
    invited_games = relationship("Game", back_populates="invitee", primaryjoin=id==Game.invitee_id) 
