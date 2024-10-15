from dataclasses import dataclass


@dataclass
class Production:
    _type: str
    name: str
    image: str
    year: int
    role: str
    company: str
