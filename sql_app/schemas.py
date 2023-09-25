from typing import List, Union

from pydantic import BaseModel


class Game(BaseModel):
    id: int
    owner_id: Union[int, None]
    invitee_id: Union[int, None]
    state: str = "---------"

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    email: str
    owned_games: List[Game] = []
    invited_games: List[Game] = []

    class Config:
        orm_mode = True
