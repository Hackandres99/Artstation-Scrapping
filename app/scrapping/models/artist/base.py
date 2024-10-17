from dataclasses import dataclass
from typing import List

@dataclass
class Base:
    artist_id: str
    resume_page: str
    followers: int
    following: int
    artworks_count: int
    interests: List[str]
