from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///dht22.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()

class ReadDHT22(Base):
    __tablename__ = "leituras"

    #Data base model
    id = Column(Integer, primary_key=True,autoincrement=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    device_id = Column(String, default="ESP32_01")
    timestamp = Column(DateTime, default=func.now())

#Create the tables in the database
Base.metadata.create_all(engine)