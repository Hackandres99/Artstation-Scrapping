from dataclasses import dataclass
from .period import Period


@dataclass
class Experience:
    role: str
    location: str
    period: Period
    description: str
