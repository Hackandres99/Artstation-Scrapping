from dataclasses import dataclass


@dataclass
class User:
    name: str
    author: bool
    avatar: str
    headline: str
