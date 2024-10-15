from dataclasses import dataclass
from typing import List
from datetime import datetime
from .comment import Comment
from ..software_proficiency import Sofware
from bson import ObjectId


@dataclass
class Artwork:
    _id: ObjectId
    title: str
    description: str
    date: datetime
    likes: int
    views: int
    threads: int
    comments: List[Comment]
    softwares: List[Sofware]
    tags: List[str]
    images: List[str]
    artist_url: str
