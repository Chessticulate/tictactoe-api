from typing import List, Union

from pydantic import BaseModel


class GameBase(BaseModel):
    title: str
    description: Union[str, None]


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int
    owner_id: int
    invitee_id: Union[int, None]
    user_to_move: Union[int, None]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    owned_games: List[Game] = []
    invited_games: List[Game] = []
    next_up_games: List[Game] = []

    class Config:
        orm_mode = True
