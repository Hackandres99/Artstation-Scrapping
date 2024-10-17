from dataclasses import dataclass
from .base import Base
from .resume import Resume


@dataclass
class Artist:
    base_info: Base
    resume_info: Resume
