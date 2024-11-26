from typing import List, Optional, Dict
from models.bookmark import Bookmark
from database.db_manager import DatabaseManager

class BookmarkRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def _get_next_sequence(self, cursor) -> int:
        cursor.execute('SELECT MAX(sequence) FROM bookmarks')
        result = cursor.fetchone()[0]
        return 1 if result is None else result + 1

    def _format_custom_id(self, sequence: int) -> str:
        return f"No.{sequence:04d}"

    def _reorder_sequences(self, cursor, start_sequence: int):
        """Reorder sequences from a starting point"""
        cursor.execute('''
            UPDATE bookmarks 
            SET sequence = sequence - 1,
                custom_id = 'No.' || substr('0000' || CAST(sequence - 1 AS TEXT), -4)
            WHERE sequence > ?
        ''', (start_sequence,))

    def add(self, bookmark: Bookmark) -> str:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get next sequence number
            sequence = self._get_next_sequence(cursor)
            custom_id = self._format_custom_id(sequence)
            
            # Insert bookmark
            cursor.execute('''
                INSERT INTO bookmarks (url, title, description, custom_id, sequence)
                VALUES (?, ?, ?, ?, ?)
            ''', (bookmark.url, bookmark.title, bookmark.description, 
                  custom_id, sequence))
            
            bookmark_id = cursor.lastrowid
            
            # Add tags
            if bookmark.tags:
                for tag in bookmark.tags:
                    cursor.execute('''
                        INSERT OR IGNORE INTO tags (name)
                        VALUES (?)
                    ''', (tag,))
                    
                    cursor.execute('SELECT id FROM tags WHERE name = ?', (tag,))
                    tag_id = cursor.fetchone()[0]
                    
                    cursor.execute('''
                        INSERT INTO bookmark_tags (bookmark_id, tag_id)
                        VALUES (?, ?)
                    ''', (bookmark_id, tag_id))
            
            conn.commit()
            return custom_id

    def delete(self, custom_id: str) -> bool:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get the sequence of the bookmark to be deleted
            cursor.execute('''
                SELECT sequence FROM bookmarks WHERE custom_id = ?
            ''', (custom_id,))
            result = cursor.fetchone()
            
            if not result:
                return False
                
            sequence = result[0]
            
            # Delete the bookmark
            cursor.execute('DELETE FROM bookmarks WHERE custom_id = ?', (custom_id,))
            
            # Reorder remaining bookmarks
            self._reorder_sequences(cursor, sequence)
            
            conn.commit()
            return True

    def get(self, custom_id: str) -> Optional[Bookmark]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT b.*, GROUP_CONCAT(t.name) as tags
                FROM bookmarks b
                LEFT JOIN bookmark_tags bt ON b.id = bt.bookmark_id
                LEFT JOIN tags t ON bt.tag_id = t.id
                WHERE b.custom_id = ?
                GROUP BY b.id
            ''', (custom_id,))
            
            row = cursor.fetchone()
            if row:
                tags = row['tags'].split(',') if row['tags'] else []
                return Bookmark(
                    id=row['id'],
                    custom_id=row['custom_id'],
                    url=row['url'],
                    title=row['title'],
                    description=row['description'],
                    tags=tags
                )
            return None
            def get_random(self) -> Optional[Bookmark]:
                with self.db_manager.get_connection() as conn:
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        SELECT b.*, GROUP_CONCAT(t.name) as tags
                        FROM bookmarks b
                        LEFT JOIN bookmark_tags bt ON b.id = bt.bookmark_id
                        LEFT JOIN tags t ON bt.tag_id = t.id
                        GROUP BY b.id
                        ORDER BY RANDOM()
                        LIMIT 1
                    ''')
                    
                    row = cursor.fetchone()
                    if row:
                        tags = row['tags'].split(',') if row['tags'] else []
                        return Bookmark(
                            id=row['id'],
                            custom_id=row['custom_id'],
                            url=row['url'],
                            title=row['title'],
                            description=row['description'],
                            tags=tags
                        )
                    return None

    def get_bookmark_count(self) -> int:
        """Get the total number of bookmarks in the database."""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT MAX(sequence) FROM bookmarks')
            result = cursor.fetchone()[0]
            return 0 if result is None else result

    def get_by_number(self, number: int) -> Optional[Bookmark]:
        """Get bookmark by number (without 'No.' prefix)"""
        custom_id = f"No.{number:04d}"
        return self.get(custom_id)

    def get_random(self) -> Optional[Bookmark]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT b.*, GROUP_CONCAT(t.name) as tags
                FROM bookmarks b
                LEFT JOIN bookmark_tags bt ON b.id = bt.bookmark_id
                LEFT JOIN tags t ON bt.tag_id = t.id
                GROUP BY b.id
                ORDER BY RANDOM()
                LIMIT 1
            ''')
            
            row = cursor.fetchone()
            if row:
                tags = row['tags'].split(',') if row['tags'] else []
                return Bookmark(
                    id=row['id'],
                    custom_id=row['custom_id'],
                    url=row['url'],
                    title=row['title'],
                    description=row['description'],
                    tags=tags
                )
            return None
