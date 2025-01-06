from models.cart import Cart, CartItem
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound


# Create a new cart for a user
def create_cart(db: Session, user_id: int):
    db_cart = Cart(user_id=user_id)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


# Add an item to the cart
def add_item_to_cart(db: Session, cart_id: int, product_id: int, quantity: int):
    # Check if the item already exists in the cart
    db_item = db.query(CartItem).filter(
        CartItem.cart_id == cart_id, CartItem.product_id == product_id
    ).first()
    if db_item:
        # Update quantity if item exists
        db_item.quantity += quantity
    else:
        # Add a new item to the cart
        db_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
        db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Get all items in a cart
def get_cart_items(db: Session, cart_id: int):
    return db.query(CartItem).filter(CartItem.cart_id == cart_id).all()


# Update the quantity of an item in the cart
def update_cart_item_quantity(db: Session, cart_id: int, product_id: int, new_quantity: int):
    db_item = db.query(CartItem).filter(
        CartItem.cart_id == cart_id, CartItem.product_id == product_id
    ).first()
    if not db_item:
        raise NoResultFound(f"Item with product_id {product_id} not found in cart {cart_id}")
    if new_quantity <= 0:
        # Remove item if quantity is zero or less
        db.delete(db_item)
    else:
        # Update the quantity
        db_item.quantity = new_quantity
    db.commit()
    return db_item


# Remove an item from the cart
def remove_item_from_cart(db: Session, cart_id: int, product_id: int):
    db_item = db.query(CartItem).filter(
        CartItem.cart_id == cart_id, CartItem.product_id == product_id
    ).first()
    if not db_item:
        raise NoResultFound(f"Item with product_id {product_id} not found in cart {cart_id}")
    db.delete(db_item)
    db.commit()
    return {"message": f"Item with product_id {product_id} removed from cart {cart_id}"}


# Clear all items from a cart
def clear_cart(db: Session, cart_id: int):
    db_items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()
    if not db_items:
        return {"message": f"Cart {cart_id} is already empty"}
    for item in db_items:
        db.delete(item)
    db.commit()
    return {"message": f"All items removed from cart {cart_id}"}
