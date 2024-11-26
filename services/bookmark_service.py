from typing import List, Optional
from models.bookmark import Bookmark
from repositories.bookmark_repository import BookmarkRepository
import json

class BookmarkService:
    def __init__(self, repository: BookmarkRepository):
        self.repository = repository

    def add_bookmark(self, url: str, title: str = None, description: str = None,
                    tags: List[str] = None) -> str:
        bookmark = Bookmark(
            url=url,
            custom_id="",  # Will be set by repository
            title=title,
            description=description,
            tags=tags
        )
        return self.repository.add(bookmark)

    def delete_bookmark(self, custom_id: str) -> bool:
        return self.repository.delete(custom_id)

    def get_bookmark(self, custom_id: str) -> Optional[Bookmark]:
        return self.repository.get(custom_id)

    def get_random_bookmark(self) -> Optional[Bookmark]:
        """Get a random bookmark from the database."""
        return self.repository.get_random()

    def get_bookmark_count(self) -> int:
        """Get the total number of bookmarks."""
        return self.repository.get_bookmark_count()

    def get_bookmark_by_number(self, number: int) -> Optional[Bookmark]:
        """Get bookmark by number."""
        return self.repository.get_by_number(number)