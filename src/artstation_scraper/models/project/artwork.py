from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime
from .comment import Comment


@dataclass
class Artwork:
    title: str
    description: str
    date: datetime
    likes: int
    views: int
    threads: int
    comments: List[Comment]
    software: Dict[str, str]
    tags: List[str]
    images: List[str]
