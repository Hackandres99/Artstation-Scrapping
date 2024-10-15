from dataclasses import dataclass
from datetime import datetime


@dataclass
class Period:
    start: datetime
    end: datetime | str
