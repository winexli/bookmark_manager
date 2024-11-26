from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Bookmark:
    url: str
    custom_id: str  # Stores IDs like "No.0001"
    title: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = None
    id: Optional[int] = None  # SQLite internal ID

    def __post_init__(self):
        if self.tags is None:
            self.tags = []