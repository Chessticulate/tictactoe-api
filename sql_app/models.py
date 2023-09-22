from datetime import datetime

from sqlalchemy import Boolean, DateTime, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    owned_games = relationship("Game", back_populates="owner")
    invited_games = relationship("Game", back_populates="invitee")
    next_up_games = relationship("Game", back_populates="user_to_move")


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String, index=True)
    started_at = Column(DateTime, index=True, default=datetime.utcnow)
    state = Column(String)

    owner_id = relationship("User", back_populates="owned_games") 
    invitee_id = relationship("User", back_populates="invited_games") 
    user_to_move = relationship("User", back_populates="next_up_games")
