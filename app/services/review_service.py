# services/review_service.py
from models.review import Review
from sqlalchemy.orm import Session

def create_review(db: Session, product_id: int, user_id: int, rating: float, comment: str):
    db_review = Review(product_id=product_id, user_id=user_id, rating=rating, comment=comment)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews_for_product(db: Session, product_id: int):
    return db.query(Review).filter(Review.product_id == product_id).all()
