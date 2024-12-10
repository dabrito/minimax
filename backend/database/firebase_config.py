import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
cred = credentials.Certificate("./minimax-ae980-firebase-adminsdk-hql01-dc669291ea.json")  # Ruta al archivo JSON de tu proyecto
firebase_admin.initialize_app(cred)
db = firestore.client()

# # Clase Product
# class Product:
#     def __init__(self, id=None, name="", cost=0.0, rival_price=0.0, initial_price=0.0, min_price=0.0, max_price=0.0):
#         self.id = id
#         self.name = name
#         self.cost = cost
#         self.rival_price = rival_price
#         self.initial_price = initial_price
#         self.min_price = min_price
#         self.max_price = max_price

#     def to_dict(self):
#         return {
#             "name": self.name,
#             "cost": self.cost,
#             "rival_price": self.rival_price,
#             "initial_price": self.initial_price,
#             "min_price": self.min_price,
#             "max_price": self.max_price,
#         }

#     @staticmethod
#     def from_dict(data, id):
#         return Product(
#             id=id,
#             name=data.get("name", ""),
#             cost=data.get("cost", 0.0),
#             rival_price=data.get("rival_price", 0.0),
#             initial_price=data.get("initial_price", 0.0),
#             min_price=data.get("min_price", 0.0),
#             max_price=data.get("max_price", 0.0),
#         )

# # Funciones CRUD
# def add_product(product: Product):
#     doc_ref = db.collection("products").add(product.to_dict())
#     print(f"Producto agregado con ID: {doc_ref[1].id}")

# def get_product(product_id: str):
#     doc = db.collection("products").document(product_id).get()
#     if doc.exists:
#         product = Product.from_dict(doc.to_dict(), doc.id)
#         print("Producto obtenido:", product.__dict__)
#         return product
#     else:
#         print("Producto no encontrado")
#         return None

# def update_product(product_id: str, updates: dict):
#     db.collection("products").document(product_id).update(updates)
#     print("Producto actualizado")

# def delete_product(product_id: str):
#     db.collection("products").document(product_id).delete()
#     print("Producto eliminado")

# def list_products():
#     docs = db.collection("products").stream()
#     products = [Product.from_dict(doc.to_dict(), doc.id) for doc in docs]
#     for product in products:
#         print(product.__dict__)
#     return products