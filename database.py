from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database file used by the application.
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

# Engine configuration for SQLite.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Session factory for request-scoped database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    # FastAPI dependency: provide a DB session and always close it after request.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
