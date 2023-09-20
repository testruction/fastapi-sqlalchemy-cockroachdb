from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backendservice.config import ProductionConfig

engine = create_engine(url=ProductionConfig.SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(bind=engine,
                            autoflush=False,
                            autocommit=False)
