from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from airflow.models import Variable

engine = create_engine(Variable.get("SQLALCHEMY_DATABASE_URL"))
SessionLocal: sessionmaker = sessionmaker(autoflush=True, autocommit=True, bind=engine)
