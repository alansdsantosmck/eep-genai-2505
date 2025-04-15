import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Retrieve the database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Setup SQLAlchemy
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Example Model
class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    skills = Column(String, nullable=False)
    is_staffed = Column(Boolean, nullable=False)
    staffing_end_date = Column(Date, nullable=True)
    years_experience = Column(Integer, nullable=False)
    industry_experience = Column(String, nullable=False)
    location = Column(String, nullable=False)