from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///dg_store.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.create_all(engine)
