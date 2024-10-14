from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    text: str
    likes: int
    date: datetime