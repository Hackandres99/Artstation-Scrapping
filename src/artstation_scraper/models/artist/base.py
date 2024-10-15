from dataclasses import dataclass
from typing import List


@dataclass
class Base:
    resume_page: str
    followers: int
    following: int
    interests: List[str]
    artwork_urls: List[str]
