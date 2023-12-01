from flask import current_app as app

class Review:
    def __init__(self, review_id, product_id, user_id, rating, comment, timestamp, upvotes):
        self.review_id = review_id
        self.product_id = product_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        self.timestamp = timestamp
        self.upvotes = upvotes

    @staticmethod
    def five_most_recent_by_user_id(uid):
        print("The product_id is: ", uid)
        rows = app.db.execute('''
SELECT review_id, product_id, user_id, rating, comment, timestamp, upvotes
FROM Review
WHERE user_id = :uid
ORDER BY timestamp DESC
LIMIT 5
''',
                              uid=uid)
        return [Review(*row) for row in rows]

    

    @staticmethod
    def find_by_user_and_product(user_id, product_id):
        rows = app.db.execute('''
SELECT review_id
FROM Review
WHERE user_id = :user_id AND product_id = :product_id
''',
                              user_id=user_id,
                              product_id=product_id)
        return rows

    @staticmethod
    def create_review(product_id, user_id, rating, comment):
        # This method will create a new review after checking if one doesn't already exist
        existing_review = Review.find_by_user_and_product(user_id, product_id)
        if existing_review:
            raise ValueError("User has already reviewed this product.")
        
        result = app.db.execute('''
INSERT INTO Review (product_id, user_id, rating, comment)
VALUES (:product_id, :user_id, :rating, :comment)
RETURNING review_id
''',
                                product_id=product_id,
                                user_id=user_id,
                                rating=rating,
                                comment=comment)
        return result

    @staticmethod
    def get_paginated_reviews(page, per_page=10, user_id=None):
        offset = (page - 1) * per_page
        query = '''
SELECT review_id, product_id, user_id, rating, comment, timestamp, upvotes
FROM Review
'''
        params = {
            'per_page': per_page,
            'offset': offset
        }
        if user_id:
            query += 'WHERE user_id = :user_id\n'
            params['user_id'] = user_id
        query += 'ORDER BY timestamp DESC\nLIMIT :per_page OFFSET :offset'
        rows = app.db.execute(query, **params)
        return [Review(*row) for row in rows]

    @staticmethod
    def get_paginated_reviews_by_product_id(k, n, product_id, ftr=None, ord=None):
        k *= n
        rows = app.db.execute('''
SELECT review_id, product_id, user_id, rating, comment, timestamp, upvotes
FROM Review
WHERE product_id = :product_id
''' + (f'ORDER BY {ftr} {ord}' if ord is not None else '') + '''
OFFSET :k ROWS FETCH NEXT :n ROWS ONLY
''',
                              product_id=product_id,
                              k=k,
                              n=n)
        return [Review(*row) for row in rows]


    
    @staticmethod
    def count_reviews_by_product_id(product_id):
        rows = app.db.execute('''
SELECT COUNT(*)
FROM Review
WHERE product_id = :product_id
''',
                                product_id=product_id)
        return rows[0][0] if rows else 0

    @staticmethod
    def count_all_reviews(user_id=None):
        query = 'SELECT COUNT(*) FROM Review'
        params = {}
        if user_id:
            query += ' WHERE user_id = :user_id'
            params['user_id'] = user_id
        rows = app.db.execute(query, **params)
        return rows[0][0] if rows else 0
