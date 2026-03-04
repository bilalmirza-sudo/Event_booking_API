from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import User


def require_user_by_user_id(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def require_admin_by_user_id(user_id: int, db: Session) -> User:
    user = require_user_by_user_id(user_id=user_id, db=db)
    if user.role.lower() != "admin":
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to perform this action",
        )
    return user