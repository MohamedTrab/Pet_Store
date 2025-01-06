from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models.category import Category


# Create a new category
def create_category(db: Session, name: str):
    # Check if category already exists
    existing_category = db.query(Category).filter(
        Category.name == name).first()
    if existing_category:
        return existing_category  # Or raise an exception if needed

    # Create and add new category
    new_category = Category(name=name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


# Get all categories
def get_all_categories(db: Session):
    return db.query(Category).all()


# Get a category by ID
def get_category_by_id(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise NoResultFound(f"Category with ID {category_id} not found")
    return category


# Update a category
def update_category(db: Session, category_id: int, new_name: str):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise NoResultFound(f"Category with ID {category_id} not found")

    # Check if the new name already exists
    if db.query(Category).filter(Category.name == new_name).first():
        raise ValueError(f"Category with name '{new_name}' already exists")

    category.name = new_name
    db.commit()
    db.refresh(category)
    return category


# Delete a category
def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise NoResultFound(f"Category with ID {category_id} not found")
    db.delete(category)
    db.commit()
    return {"message": f"Category with ID {category_id} has been deleted"}
