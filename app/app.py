from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from services import (
    product_service, cart_service, order_service,
    review_service, pet_service, category_service
)
from auth.auth_helper import authenticate_user, create_jwt_token, hash_password
from auth.role_based_access import role_required
from pydantic import BaseModel
from models.db import engines, Base, get_users_db, get_products_db, get_orders_db, get_reviews_db, get_pets_db
from models.user import User
from pydantic_models.category import CategoryCreate, CategoryResponse
from fastapi.openapi.models import OpenAPI
from fastapi.security import OAuth2PasswordRequestForm
app = FastAPI()
from models.user import User
import pika
from typing import List
import pika

# Initialize database tables
for bind_key, engine in engines.items():
    print(f"Creacion de tablas para : {bind_key}")
    Base.metadata.create_all(bind=engine)


# Login and registration models
class LoginData(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str
    address: str
    role: str


RABBITMQ_HOST = "rabbitmq"
RABBITMQ_HOST_ = "localhost"
QUEUE_NAME = "user_registration"
CART_QUEUE_NAME = "cart_creation"
CATEGORY_QUEUE_NAME = "category_creation"



def get_rabbitmq_channel(queue_name: str):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        return channel
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error de conexion para RabbitMQ : {e}")
        raise


# Authentication and Registration
"""
@app.post("/token")
def login_for_access_token(login_data: LoginData, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt_token(user)
    return {"access_token": token, "token_type": "bearer"}
"""
"""
@app.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    
    # Generar token para cualquier usuario autenticado
    token = create_jwt_token(user)
    return {"access_token": token, "token_type": "bearer"}
"""

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_users_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt_token(user)
    return {"access_token": token, "token_type": "bearer"}





@app.post("/register/")
def register(request: RegisterRequest, db: Session = Depends(get_users_db)):
    # Check if the username already exists
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password
    hashed_password = hash_password(request.password)

    # Create a new user with role and address
    new_user = User(
        username=request.username,
        password=hashed_password,
        address=request.address,
        role=request.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Publish a message to RabbitMQ
    rabbitmq_channel = get_rabbitmq_channel(QUEUE_NAME)
    rabbitmq_channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=f"Nouvel utilisateur enregistré : {new_user.username} avec le rôle {new_user.role}"
    )

    return {
        "message": "User registered successfully",
        "user": {
            "username": new_user.username,
            "address": new_user.address,
            "role": new_user.role
        }
    }

from typing import List

@app.get("/users/", response_model=List[RegisterRequest])
def get_all_users(db: Session = Depends(get_users_db)):
    users = db.query(User).all()
    return users

@app.put("/users/{user_id}/")
def update_user(user_id: int, request: RegisterRequest, db: Session = Depends(get_users_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = request.username
    user.password = hash_password(request.password) 
    user.address = request.address
    user.role = request.role

    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "user": {
        "username": user.username,
        "address": user.address,
        "role": user.role
    }}



# Products Routes
@app.post("/products/", dependencies=[Depends(role_required('admin'))])
def create_product(name: str, description: str, price: float, category_id: int, stock: int, images: str, db: Session = Depends(get_products_db)):
    return product_service.create_product(db, name, description, price, category_id, stock, images)


@app.get("/products/", dependencies=[Depends(role_required('admin'))])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_products_db)):
    return product_service.get_products(db, skip, limit)


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_products_db)):
    product = product_service.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/products/search/")
def search_products(
    name: str = None, category: str = None, min_price: float = None, max_price: float = None, db: Session = Depends(get_products_db)
):
    return product_service.search_products(db, name, category, min_price, max_price)


@app.post("/carts/")
def create_cart(user_id: int, db: Session = Depends(get_users_db)):
    # Appeler le service pour créer le panier
    cart = cart_service.create_cart(db, user_id)

    # Envoyer un message à RabbitMQ
    rabbitmq_channel = get_rabbitmq_channel(CART_QUEUE_NAME)
    rabbitmq_channel.basic_publish(
        exchange='',
        routing_key=CART_QUEUE_NAME,
        body=f"Se ha creado un nuevo carrito para el usuario : {user_id}"
    )

    return {"message": "Cart created successfully", "cart_id": cart.id}


@app.post("/carts/{cart_id}/items")
def add_item_to_cart(cart_id: int, product_id: int, quantity: int, db: Session = Depends(get_users_db)):
    return cart_service.add_item_to_cart(db, cart_id, product_id, quantity)


@app.get("/carts/{cart_id}/items")
def get_cart_items(cart_id: int, db: Session = Depends(get_users_db)):
    return cart_service.get_cart_items(db, cart_id)


# Orders Routes
@app.post("/orders/")
def create_order(user_id: int, total_price: float, db: Session = Depends(get_users_db)):
    return order_service.create_order(db, user_id, total_price)


@app.get("/orders/{order_id}")
def get_order_by_id(order_id: int, db: Session = Depends(get_orders_db)):
    order = order_service.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.get("/orders/user/{user_id}")
def get_orders_by_user(user_id: int, db: Session = Depends(get_orders_db)):
    return order_service.get_order_by_id(db, user_id)


# Reviews Routes
@app.post("/reviews/")
def create_review(product_id: int, user_id: int, rating: float, comment: str, db: Session = Depends(get_reviews_db)):
    return review_service.create_review(db, product_id, user_id, rating, comment)


@app.get("/reviews/{product_id}")
def get_reviews_for_product(product_id: int, db: Session = Depends(get_pets_db)):
    return review_service.get_reviews_for_product(db, product_id)


# Pets Routes
@app.post("/pets/")
def create_pet(name: str, pet_type: str, age: int, price: float, user_id: int, db: Session = Depends(get_pets_db)):
    return pet_service.create_pet(db, name, pet_type, age, price, user_id)


@app.get("/pets/{user_id}")
def get_pets_by_user(user_id: int, db: Session = Depends(get_pets_db)):
    return pet_service.get_pets_by_user(db, user_id)


# Categories Routes
@app.post("/categories/", response_model=CategoryResponse, dependencies=[Depends(role_required('admin'))])
def create_category(request: CategoryCreate, db: Session = Depends(get_products_db)):
    # Appeler le service pour créer la catégorie
    category = category_service.create_category(db, request.name)
    if category is None:
        raise HTTPException(status_code=400, detail="Category already exists")

    # Envoyer un message à RabbitMQ
    rabbitmq_channel = get_rabbitmq_channel(CATEGORY_QUEUE_NAME)
    rabbitmq_channel.basic_publish(
        exchange='',
        routing_key=CATEGORY_QUEUE_NAME,
        body=f"Nouvelle catégorie créée : {category.name}"
    )

    return category



@app.get("/categories/")
def get_categories(db: Session = Depends(get_products_db)):
    return category_service.get_all_categories(db)


@app.get("/categories/{category_id}")
def get_category_by_id(category_id: int, db: Session = Depends(get_products_db)):
    category = category_service.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# Products Routes
@app.put("/products/{product_id}", dependencies=[Depends(role_required('admin'))])
def update_product(
    product_id: int,
    name: str = None,
    description: str = None,
    price: float = None,
    category_id: int = None,
    stock: int = None,
    images: str = None,
    db: Session = Depends(get_products_db),
):
    updated_product = product_service.update_product(
        db, product_id, name, description, price, category_id, stock, images
    )
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@app.delete("/products/{product_id}", dependencies=[Depends(role_required('admin'))])
def delete_product(product_id: int, db: Session = Depends(get_products_db)):
    result = product_service.delete_product(db, product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# Cart Routes


@app.put("/carts/{cart_id}/items/{item_id}", dependencies=[Depends(role_required('admin'))])
def update_cart_item(
    cart_id: int, item_id: int, quantity: int, db: Session = Depends(get_users_db)
):
    updated_item = cart_service.update_cart_item(
        db, cart_id, item_id, quantity)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return updated_item


@app.delete("/carts/{cart_id}/items/{item_id}", dependencies=[Depends(role_required('admin'))])
def delete_cart_item(cart_id: int, item_id: int, db: Session = Depends(get_users_db)):
    result = cart_service.delete_cart_item(db, cart_id, item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Cart item deleted successfully"}

# Orders Routes


@app.put("/orders/{order_id}", dependencies=[Depends(role_required('admin'))])
def update_order(
    order_id: int,
    total_price: float = None,
    status: str = None,
    db: Session = Depends(get_orders_db),
):
    updated_order = order_service.update_order(
        db, order_id, total_price, status)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order


@app.delete("/orders/{order_id}", dependencies=[Depends(role_required('admin'))])
def delete_order(order_id: int, db: Session = Depends(get_orders_db)):
    result = order_service.delete_order(db, order_id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

# Reviews Routes


@app.put("/reviews/{review_id}", dependencies=[Depends(role_required('admin'))])
def update_review(
    review_id: int,
    rating: float = None,
    comment: str = None,
    db: Session = Depends(get_reviews_db),
):
    updated_review = review_service.update_review(
        db, review_id, rating, comment)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review


@app.delete("/reviews/{review_id}", dependencies=[Depends(role_required('admin'))])
def delete_review(review_id: int, db: Session = Depends(get_reviews_db)):
    result = review_service.delete_review(db, review_id)
    if not result:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}

# Pets Routes


@app.put("/pets/{pet_id}", dependencies=[Depends(role_required('admin'))])
def update_pet(
    pet_id: int,
    name: str = None,
    pet_type: str = None,
    age: int = None,
    price: float = None,
    db: Session = Depends(get_pets_db),
):
    updated_pet = pet_service.update_pet(
        db, pet_id, name, pet_type, age, price)
    if not updated_pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return updated_pet


@app.delete("/pets/{pet_id}", dependencies=[Depends(role_required('admin'))])
def delete_pet(pet_id: int, db: Session = Depends(get_pets_db)):
    result = pet_service.delete_pet(db, pet_id)
    if not result:
        raise HTTPException(status_code=404, detail="Pet not found")
    return {"message": "Pet deleted successfully"}

# Categories Routes


@app.put("/categories/{category_id}", dependencies=[Depends(role_required('admin'))])
def update_category(
    category_id: int, name: str, db: Session = Depends(get_products_db)
):
    updated_category = category_service.update_category(db, category_id, name)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category


@app.delete("/categories/{category_id}", dependencies=[Depends(role_required('admin'))])
def delete_category(category_id: int, db: Session = Depends(get_products_db)):
    result = category_service.delete_category(db, category_id)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

# Swagger YAML Endpoint

# User Routes


@app.get("/users/{username}", dependencies=[Depends(role_required('admin'))])
def get_user_by_username(username: str, db: Session = Depends(get_users_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username}


@app.put("/users/{user_id}", dependencies=[Depends(role_required('admin'))])
def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    db: Session = Depends(get_users_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields if provided
    if username:
        existing_user = db.query(User).filter(
            User.username == username).first()
        if existing_user:
            raise HTTPException(
                status_code=400, detail="Username already exists")
        user.username = username

    if password:
        user.password = hash_password(password)

    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "user": {"username": user.username}}


@app.get("/swagger.yaml", response_model=OpenAPI)
async def get_swagger_yaml():
    with open("swagger.yaml", "r") as f:
        return f.read()
