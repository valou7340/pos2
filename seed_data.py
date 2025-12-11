# database/seed_data.py
from sqlalchemy.orm import Session
from database.models import Base, Category, Product, Employee
from config.database import engine
import bcrypt

def init_db():
    Base.metadata.create_all(bind=engine)

    from config.database import SessionLocal
    db: Session = SessionLocal()

    # Catégories
    cats = ["Entrées", "Plats", "Desserts", "Boissons", "Vins", "Cafés"]
    for cat in cats:
        if not db.query(Category).filter(Category.name == cat).first():
            db.add(Category(name=Category(name=cat))
    db.commit()

    # Produits exemples
    if not db.query(Product).first():
        plats = db.query(Category).filter(Category.name == "Plats").first()
        db.add_all([
            Product(name="Steak Frites", price_ht=15.45, category=plats),
            Product(name="Salade César", price_ht=11.80, category=plats),
            Product(name="Mojito", price_ht=8.18, category=db.query(Category).filter(Category.name == "Boissons").first()),
            Product(name="Tiramisu", price_ht=6.36, category=db.query(Category).filter(Category.name == "Desserts").first()),
        ])
        db.commit()

    # Admin par défaut PIN = 1234
    if not db.query(Employee).first():
        hashed = bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt())
        db.add(Employee(name="Admin", pin=hashed.decode('utf-8'), is_admin=True))
        db.commit()

    db.close()
    print("Base de données initialisée avec succès !")
