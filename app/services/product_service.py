from models.product import Product
from models.category import Category
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List, Optional
from fastapi import HTTPException


# Create a new product
def create_product(
    db: Session, name: str, description: str, price: float,
    category_id: int, stock: int, images: str
):
    # Validate category existence
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Create and save the product
    db_product = Product(
        name=name, description=description, price=price,
        category_id=category_id, stock=stock, images=images
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Get a product by ID
def get_product_by_id(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Get all products with pagination
def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()


# Search products with filters
def search_products(
    db: Session, name: Optional[str] = None, category: Optional[str] = None,
    min_price: Optional[float] = None, max_price: Optional[float] = None
) -> List[Product]:
    query = db.query(Product)

    # Apply filters based on the query parameters
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if category:
        query = query.join(Category).filter(Category.name == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    return query.all()


# Update a product
def update_product(
    db: Session, product_id: int, name: Optional[str] = None,
    description: Optional[str] = None, price: Optional[float] = None,
    category_id: Optional[int] = None, stock: Optional[int] = None,
    images: Optional[str] = None
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if name:
        product.name = name
    if description:
        product.description = description
    if price:
        product.price = price
    if category_id:
        category = db.query(Category).filter(
            Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        product.category_id = category_id
    if stock is not None:
        product.stock = stock
    if images:
        product.images = images

    db.commit()
    db.refresh(product)
    return product


# Delete a product
def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": f"Product with ID {product_id} has been deleted"}
