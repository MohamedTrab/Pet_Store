from models.order import Order, OrderItem
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound


# Create a new order
def create_order(db: Session, user_id: int, total_price: float):
    db_order = Order(user_id=user_id, total_price=total_price)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


# Add items to an existing order
def add_items_to_order(db: Session, order_id: int, product_id: int, quantity: int):
    # Ensure the order exists
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise NoResultFound(f"Order with ID {order_id} not found")

    # Add items to the order
    db_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity)
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item


# Get all orders
def get_all_orders(db: Session):
    return db.query(Order).all()


# Get an order by ID
def get_order_by_id(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise NoResultFound(f"Order with ID {order_id} not found")
    return order


# Get all items in a specific order
def get_order_items(db: Session, order_id: int):
    # Ensure the order exists
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise NoResultFound(f"Order with ID {order_id} not found")

    return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()


# Update the total price of an order
def update_order_total_price(db: Session, order_id: int, new_total_price: float):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise NoResultFound(f"Order with ID {order_id} not found")

    order.total_price = new_total_price
    db.commit()
    db.refresh(order)
    return order


# Delete an order
def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise NoResultFound(f"Order with ID {order_id} not found")

    # Cascade deletion will automatically remove associated order items
    db.delete(order)
    db.commit()
    return {"message": f"Order with ID {order_id} has been deleted"}


# Delete a specific item from an order
def delete_order_item(db: Session, order_item_id: int):
    order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if not order_item:
        raise NoResultFound(f"Order item with ID {order_item_id} not found")

    db.delete(order_item)
    db.commit()
    return {"message": f"Order item with ID {order_item_id} has been deleted"}
