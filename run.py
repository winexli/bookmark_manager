# run.py
from database.db_manager import DatabaseManager
from repositories.bookmark_repository import BookmarkRepository
from services.bookmark_service import BookmarkService

def get_valid_number(prompt: str, max_num: int) -> int:
    """Validate user input to ensure it's a valid number within range."""
    while True:
        try:
            num = int(input(prompt))
            if 1 <= num <= max_num:
                return num
            print(f"Please enter a number between 1 and {max_num}")
        except ValueError:
            print("Please enter a valid number")

def print_menu():
    print("\nBookmark Manager Menu:")
    print("1. Add bookmark")
    print("2. Get bookmark")
    print("3. Delete bookmark")
    print("4. Random bookmark")
    print("5. Search bookmarks")
    print("6. Exit")
    print("\nEnter your choice (1-6): ")

def main():
    db_manager = DatabaseManager()
    repository = BookmarkRepository(db_manager)
    service = BookmarkService(repository)

    while True:
        print_menu()
        choice = input()

        if choice == "1":
            url = input("Enter URL: ")
            title = input("Enter title (optional, press enter to skip): ") or None
            desc = input("Enter description (optional, press enter to skip): ") or None
            tags = input("Enter tags (comma-separated, optional): ")
            tags = [t.strip() for t in tags.split(",")] if tags else None
            
            bookmark_id = service.add_bookmark(url, title, desc, tags)
            print(f"Bookmark added with ID: {bookmark_id}")

        elif choice == "2":
            total_bookmarks = service.get_bookmark_count()
            if total_bookmarks == 0:
                print("No bookmarks available")
                continue
                
            print(f"\nCurrent bookmarks: {total_bookmarks}")
            print(f"Please choose from 1 to {total_bookmarks}")
            
            number = get_valid_number("Enter bookmark number: ", total_bookmarks)
            bookmark = service.get_bookmark_by_number(number)
            
            if bookmark:
                print(f"\nID: {bookmark.custom_id}")
                print(f"Title: {bookmark.title}")
                print(f"URL: {bookmark.url}")
                print(f"Description: {bookmark.description}")
                print(f"Tags: {', '.join(bookmark.tags)}")
            else:
                print("Bookmark not found")

        elif choice == "3":
            total_bookmarks = service.get_bookmark_count()
            if total_bookmarks == 0:
                print("No bookmarks available")
                continue
                
            print(f"\nCurrent bookmarks: {total_bookmarks}")
            print(f"Please choose from 1 to {total_bookmarks}")
            
            number = get_valid_number("Enter bookmark number to delete: ", total_bookmarks)
            custom_id = f"No.{number:04d}"
            
            if service.delete_bookmark(custom_id):
                print("Bookmark deleted successfully")
            else:
                print("Bookmark not found")

        elif choice == "4":
            bookmark = service.get_random_bookmark()
            if bookmark:
                print("\nRandom bookmark selected:")
                print(f"ID: {bookmark.custom_id}")
                print(f"Title: {bookmark.title}")
                print(f"URL: {bookmark.url}")
                print(f"Description: {bookmark.description}")
                print(f"Tags: {', '.join(bookmark.tags)}")
            else:
                print("No bookmarks available")

        elif choice == "5":
            keywords = input("Enter search keywords (space-separated): ")
            if not keywords.strip():
                print("Please enter some keywords to search")
                continue
                
            results = service.search_bookmarks(keywords)
            
            if results:
                print(f"\nFound {len(results)} matching bookmarks:")
                for bookmark in results:
                    print("\n------------------------")
                    print(f"ID: {bookmark.custom_id}")
                    print(f"Title: {bookmark.title}")
                    print(f"URL: {bookmark.url}")
                    print(f"Description: {bookmark.description}")
                    print(f"Tags: {', '.join(bookmark.tags)}")
            else:
                print("No matching bookmarks found")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()