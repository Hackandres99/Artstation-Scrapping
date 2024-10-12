from dataclasses import dataclass
from typing import List, Dict
from bson import ObjectId
from datetime import datetime


@dataclass
class Artwork:
    id: ObjectId
    title: str
    description: str
    date: datetime
    likes: int
    views: int
    comments: int
    software: Dict[str, str]
    tags: List[str]
    images: List[str]
