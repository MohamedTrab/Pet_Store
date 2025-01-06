from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuration des bases de données


DATABASES_ = {
     "users": "postgresql://postgres:postgres@localhost:5432/users_db",
     "products": "postgresql://postgres:postgres@localhost:5432/products_db",
     "orders": "postgresql://postgres:postgres@localhost:5432/orders_db",
     "reviews": "postgresql://postgres:postgres@localhost:5432/reviews_db",
     "pets": "postgresql://postgres:postgres@localhost:5432/pets_db",
 }


DATABASES = {
     "users": "postgresql://postgres:postgres@dbUsers:5432/users_db",
     "products": "postgresql://postgres:postgres@dbProducts:5432/products_db",
     "orders": "postgresql://postgres:postgres@dbOrders:5432/orders_db",
     "reviews": "postgresql://postgres:postgres@dbReviews:5432/reviews_db",
     "pets": "postgresql://postgres:postgres@dbPets:5432/pets_db",
}

# Créer un moteur pour chaque base de données
engines = {key: create_engine(url, echo=True) for key, url in DATABASES.items()}

# Créer une session pour chaque base de données
SessionLocal = {key: sessionmaker(autocommit=False, autoflush=False, bind=engine) for key, engine in engines.items()}

# Base commune pour tous les modèles
Base = declarative_base()


# Gestionnaire de session par base
def get_db(bind_key: str):
    db = SessionLocal[bind_key]()
    try:
        yield db
    finally:
        db.close()

def get_users_db():
    db = SessionLocal["users"]()
    try:
        yield db
    finally:
        db.close()

def get_products_db():
    db = SessionLocal["products"]()
    try:
        yield db
    finally:
        db.close()


def get_orders_db():
    db = SessionLocal["orders",]()
    try:
        yield db
    finally:
        db.close()

def get_reviews_db():
    db = SessionLocal["reviews"]()
    try:
        yield db
    finally:
        db.close()
def get_pets_db():
    db = SessionLocal["pets"]()
    try:
        yield db
    finally:
        db.close()        
