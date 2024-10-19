from dataclasses import dataclass
from typing import List
from .experience import Experience
from .social_media import Social
from ..software_proficiency import Sofware
from .production import Production


@dataclass
class Resume:
    avatar: str
    name: str
    headline: str
    location: str
    email: str
    socials: List[Social]
    summary: str
    pdf: str
    skills: List[str]
    softwares: List[Sofware]
    productions: List[Production]
    experiences: List[Experience]
