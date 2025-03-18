from sqlalchemy.orm import Session

from app.core.database import Base, engine, get_db
from app.models import User, Task


def init_db() -> None:
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")