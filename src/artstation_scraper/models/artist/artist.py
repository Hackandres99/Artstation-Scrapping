from dataclasses import dataclass
from .base import Base
from .resume import Resume
from bson import ObjectId


@dataclass
class Artist:
    _id: ObjectId
    base_info: Base
    resume_info: Resume
