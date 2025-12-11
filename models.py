# database/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    color = Column(String(7), default="#3498db")  # pour l'UI
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price_ht = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    image = Column(String(200), nullable=True)
    shortcut_key = Column(String(10), nullable=True)  # ex: "F1", "A", "1"
    is_active = Column(Boolean, default=True)

    category = relationship("Category", back_populates="products")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    table_number = Column(String(10), nullable=True)
    total = Column(Float, default=0.0)
    status = Column(String(20), default="en_cours")  # en_cours, payee, annulee
    created_at = Column(DateTime, default=datetime.now)
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    price_at_sale = Column(Float)  # prix au moment de la vente

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    pin = Column(String(60))  # hashé avec bcrypt
    is_admin = Column(Boolean, default=False)
