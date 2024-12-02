from database.db_connection import get_connection
from models import Product

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    rows = cursor.fetchall()
    conn.close()
    products = []
    for row in rows:
        product = Product(*row)
        products.append(product)
    return products

def update_product(product):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """UPDATE productos SET name=%s, cost=%s, rival_price=%s,
            initial_price=%s, min_price=%s, max_price=%s WHERE id=%s"""
    values = (product.name, product.cost, product.rival_price,
              product.initial_price, product.min_price, product.max_price, product.id)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
