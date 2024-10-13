from dataclasses import dataclass
from datetime import datetime
from typing import List
from bson import ObjectId
from .user import User


@dataclass
class Comment:
    _id: ObjectId
    user: User
    message: str
    likes: int
    date: datetime
    nested: List['Comment']
