from backend.database.firebase_config import db
from backend.models import Product

# Agregar producto a Firebase
def add_product_to_db(product: Product):
    doc_ref = db.collection("products").add(product.to_dict())
    print(f"Producto agregado con ID: {doc_ref[1].id}")

# Obtener todos los productos desde Firebase
def get_all_products():
    docs = db.collection("products").stream()
    return [Product.from_dict(doc.to_dict(), doc.id) for doc in docs]

# Actualizar un producto en Firebase
def update_product_in_db(product: Product):
    if not product.id:
        raise ValueError("El producto debe tener un ID para ser actualizado.")
    db.collection("products").document(product.id).set(product.to_dict(), merge=True)
    print(f"Producto con ID {product.id} actualizado.")

# Eliminar un producto de Firebase
def delete_product_from_db(product_id: str):
    db.collection("products").document(product_id).delete()
    print(f"Producto con ID {product_id} eliminado.")
