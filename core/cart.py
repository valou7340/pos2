# core/cart.py
from typing import List
from database.models import Product, OrderItem

class Cart:
    def __init__(self):
        self.items: List[dict] = []  # {product, quantity, price_at_sale}

    def add_product(self, product: Product, quantity: int = 1):
        for item in self.items:
            if item["product"].id == product.id:
                item["quantity"] += quantity
                return
        self.items.append({
            "product": product,
            "quantity": quantity,
            "price_at_sale": product.price_ht * 1.10  # TTC 10%
        })

    def remove_product(self, product_id: int):
        self.items = [i for i in self.items if i["product"].id != product_id]

    def get_total(self) -> float:
        return round(sum(item["quantity"] * item["price_at_sale"] for item in self.items), 2)

    def clear(self):
        self.items.clear()
