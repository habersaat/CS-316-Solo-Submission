from flask import current_app as app

# Tag model
class Tag:
    def __init__(self, id, pid, name):
        self.id = id
        self.pid = pid
        self.name = name

    # Get all tags associated with a product
    @staticmethod
    def get_tags_by_pid(pid):
        rows = app.db.execute('''
SELECT id, pid, name
FROM Tags
WHERE pid = :pid
''',
                                pid=pid)
        return [Tag(*row) for row in rows]
    
    # Get all tag names associated with a product
    @staticmethod
    def get_tagnames_by_pid(pid):
        rows = app.db.execute('''
SELECT name
FROM Tags
WHERE pid = :pid
''',
                                pid=pid)
        return [row[0] for row in rows]
    
    # Get all tags that match a query
    @staticmethod
    def get_tag_by_query(query):
        rows = app.db.execute('''
SELECT id, pid, name
FROM Tags
WHERE tag = :query
''',
                              query=query)
        return [Tag(*row) for row in rows]