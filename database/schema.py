SCHEMA_QUERIES = [
    '''
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        custom_id TEXT UNIQUE NOT NULL,
        url TEXT NOT NULL,
        title TEXT,
        description TEXT,
        sequence INTEGER UNIQUE NOT NULL  -- Used for maintaining order
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS bookmark_tags (
        bookmark_id INTEGER,
        tag_id INTEGER,
        FOREIGN KEY (bookmark_id) REFERENCES bookmarks (id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE,
        PRIMARY KEY (bookmark_id, tag_id)
    )
    ''',
    'CREATE INDEX IF NOT EXISTS idx_bookmark_sequence ON bookmarks(sequence)',
    'CREATE INDEX IF NOT EXISTS idx_bookmark_custom_id ON bookmarks(custom_id)'
]
