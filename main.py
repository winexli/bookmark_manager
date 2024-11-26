from database.db_manager import DatabaseManager
from repositories.bookmark_repository import BookmarkRepository
from services.bookmark_service import BookmarkService

def main():
    # Initialize the application
    db_manager = DatabaseManager()
    repository = BookmarkRepository(db_manager)
    service = BookmarkService(repository)

    # Example usage
    # Add some bookmarks
    id1 = service.add_bookmark(
        url="https://example1.com",
        title="Example 1",
        description="First example"
    )
    print(f"Added bookmark with ID: {id1}")  # Will print "No.0001"

    id2 = service.add_bookmark(
        url="https://example2.com",
        title="Example 2",
        description="Second example"
    )
    print(f"Added bookmark with ID: {id2}")  # Will print "No.0002"

    # Get a random bookmark
    random_bookmark = service.get_random_bookmark()
    if random_bookmark:
        print(f"Random bookmark selected: {random_bookmark.title} - {random_bookmark.url}")
    else:
        print("No bookmarks available")

if __name__ == "__main__":
    main()