from dataclasses import dataclass


@dataclass
class Preview:
    artwork_id: str
    order: int
    title: str
    image: str
    url: str
