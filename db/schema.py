from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, func
from sqlalchemy.orm import declarative_base

engine = create_engine("sqlite:///dht22.db")
Base = declarative_base()

class LeituraDHT22(Base):
    __tablename__ = "leituras"

    #Modelo para a base de dados.
    id = Column(Integer, primary_key=True)
    temperatura = Column(Float, nullable=False)
    umidade = Column(Float, nullable=False)
    device_id = Column(String, default="ESP32_01")
    timestamp = Column(DateTime, default=func.now())

#Criação da base com a tabela definida pelo modelo.
Base.metadata.create_all(engine)