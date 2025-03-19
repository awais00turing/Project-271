from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.user import User
from app.crud.user import get_user_by_id

# Update the tokenUrl to match your actual endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """Get the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Add some debug logging
        print(f"Decoding token: {token[:10]}...")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
        print(f"User ID from token: {user_id}")
    except JWTError as e:
        print(f"JWT Error: {str(e)}")
        raise credentials_exception
    
    user = get_user_by_id(db, int(user_id))
    if user is None:
        print(f"User with ID {user_id} not found in database")
        raise credentials_exception
    
    return user