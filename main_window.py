# ui/main_window.py
import customtkinter as ctk
from database.models import Product, Category
from config.database import SessionLocal
from core.cart import Cart
from utils.helpers import format_price

class MainWindow(ctk.CTk):
    def __init__(self, employee):
        super().__init__()
        self.title(f"{employee.name} - Le Bon Plat")
        self.geometry("1024x768")
        self.cart = Cart()

        # Grille gauche : catégories + produits
        left_frame = ctk.CTkFrame(self)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Panier droit
        right_frame = ctk.CTkFrame(self, width=350)
        right_frame.pack(side="right", fill="y", padx=10, pady=10)
        right_frame.pack_propagate(False)

        ctk.CTkLabel(right_frame, text="PANIER", font=("Helvetica", 24)).pack(pady=10)
        self.cart_listbox = ctk.CTkTextbox(right_frame, width=320)
        self.cart_listbox.pack(pady=10, padx=10, fill="both", expand=True)

        self.total_label = ctk.CTkLabel(right_frame, text="Total : 0,00 €", font=("Helvetica", 28))
        self.total_label.pack(pady=20)

        ctk.CTkButton(right_frame, text="PAYER", fg_color="green", hover_color="darkgreen",
                      height=80, font=("Helvetica", 32), command=self.pay).pack(pady=20)

        self.load_categories(left_frame)

    def load_categories(self, parent):
        db = SessionLocal()
        categories = db.query(Category).all()
        for cat in categories:
            btn = ctk.CTkButton(parent, text=cat.name, fg_color=cat.color or "#3498db",
                                height=60, font=("Helvetica", 18),
                                command=lambda c=cat: self.load_products(c))
            btn.pack(fill="x", pady=5, padx=10)
        db.close()

    def load_products(self, category):
        # On recrée la zone produits
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self.winfo_children()[-1]:
                widget.destroy()

        products_frame = ctk.CTkScrollableFrame(self)
        products_frame.pack(side="left", fill="both", expand=True, padx=10)

        db = SessionLocal()
        products = db.query(Product).filter_by(category_id=category.id, is_active=True).all()
        for product in products:
            btn = ctk.CTkButton(products_frame, text=f"{product.name}\n{format_price(product.price_ht * 1.10)}",
                                height=100, font=("Helvetica", 16),
                                command=lambda p=product: self.add_to_cart(p))
            btn.pack(fill="x", pady=8, padx=10)
        db.close()

    def add_to_cart(self, product):
        self.cart.add_product(product)
        self.update_cart_display()

    def update_cart_display(self):
        self.cart_listbox.delete("1.0", "end")
        for item in self.cart.items:
            line = f"{item['quantity']}x {item['product'].name}  {format_price(item['price_at_sale'] * item['quantity'])}\n"
            self.cart_listbox.insert("end", line)
        self.total_label.configure(text=f"Total : {format_price(self.cart.get_total())}")

    def pay(self):
        if self.cart.get_total() == 0:
            return
        # Ici on ajoutera le module de paiement
        ctk.messagebox.showinfo("Paiement", f"Paiement de {format_price(self.cart.get_total())} effectué !")
        self.cart.clear()
        self.update_cart_display()
