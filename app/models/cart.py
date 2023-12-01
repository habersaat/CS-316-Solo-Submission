from app.models.product import Product
from flask import current_app as app


class Cart:
    def __init__(self, uid, pid, quantity):
        #self.id = id
        self.uid = uid
        self.pid = pid
        self.quantity = quantity

    @staticmethod
    def items_by_uid(uid):
        rows = app.db.execute('''
SELECT Products.id, Products.name, Products.description_short, Products.description_long, 
Products.rating, Products.image_url, Products.price, Products.available
FROM Products, Carts
WHERE Carts.uid = :uid AND Carts.pid = Products.id
''',
                              uid=uid)
        return [Product(*row) for row in rows]
    
    #write a sql to add a row to the current cart
    #take in current user ID, add a row in the cart
    @staticmethod
    def add_to_cart(uid, pid):
        app.db.execute('''
        INSERT INTO Carts(uid, pid, quantity)
        VALUES(:uid, :pid, :quantity)
        ''',
        uid=uid,
        pid=pid,
        quantity=1)
        return
    
    @staticmethod
    def delete_from_cart(uid, pid):
        app.db.execute('''
        DELETE from Carts where uid = :uid AND pid = :pid''',
        uid = uid,
        pid = pid)
        return