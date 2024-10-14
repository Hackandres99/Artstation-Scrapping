from dataclasses import dataclass
from typing import List
from bson import ObjectId
from .user import User
from .message import Message


@dataclass
class Comment:
    _id: ObjectId
    user: User
    message: Message
    nested: List['Comment']
