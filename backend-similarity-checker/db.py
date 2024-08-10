from sqlalchemy import create_engine
from sqlalchemy.orm  import sessionmaker
from models.base import Base
from models import Project
username = 'admin'
password = 'admin1234'
host = 'localhost'
port = '5432'
db_name = 'projectDB'

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"

# create the engine to establish the connection
engine = create_engine(DATABASE_URL)

# create a session factory
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# create the tables with database
Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    # once the control returns, close the db to stop data leak and useless resource consumption
    finally:
        db.close()
