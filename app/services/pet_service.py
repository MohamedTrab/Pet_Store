from models.pet import Pet
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

# Create a new pet


def create_pet(db: Session, name: str, pet_type: str, age: int, price: float, user_id: int):
    db_pet = Pet(name=name, type=pet_type, age=age,
                 price=price, user_id=user_id)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


# Get all pets for a specific user
def get_pets_by_user(db: Session, user_id: int):
    return db.query(Pet).filter(Pet.user_id == user_id).all()


# Get all pets
def get_all_pets(db: Session):
    return db.query(Pet).all()


# Get a pet by ID
def get_pet_by_id(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise NoResultFound(f"Pet with ID {pet_id} not found")
    return pet


# Update a pet's details
def update_pet(db: Session, pet_id: int, name: str = None, pet_type: str = None, age: int = None, price: float = None):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise NoResultFound(f"Pet with ID {pet_id} not found")

    if name:
        pet.name = name
    if pet_type:
        pet.type = pet_type
    if age:
        pet.age = age
    if price:
        pet.price = price

    db.commit()
    db.refresh(pet)
    return pet


# Delete a pet by ID
def delete_pet(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise NoResultFound(f"Pet with ID {pet_id} not found")

    db.delete(pet)
    db.commit()
    return {"message": f"Pet with ID {pet_id} has been deleted"}
