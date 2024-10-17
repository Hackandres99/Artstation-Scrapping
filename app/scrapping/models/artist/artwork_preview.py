from dataclasses import dataclass


@dataclass
class Preview:
    id: str
    order: int
    title: str
    image: str
    url: str
