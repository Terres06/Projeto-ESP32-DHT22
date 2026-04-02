from typing import Optional
from fastapi import FastAPI, Depends
from db.schema import ReadDHT22, Session
from sqlalchemy import func
from datetime import datetime, date, timedelta

app = FastAPI()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@app.get("/sensor-readings")

#endpoint to retrieve all sensor readings with pagination and optional device_id filter
def get_sensor_readings(db = Depends(get_db), limit: int = 100, offset: int = 0, device_id: Optional[str] = None):
    try:
        query = db.query(ReadDHT22)
        if device_id:
            query = query.filter(ReadDHT22.device_id == device_id)
        read = query.offset(offset).limit(limit).all()
        return [{k: v for k, v in reading.__dict__.items() if k != "_sa_instance_state"} for reading in read]
    except Exception as e:
        return {"error": str(e)}

@app.get("/last-reading")

#endpoint to retrieve the last sensor reading for a specific device_id or the most recent reading if no device_id is provided
def get_last_reading(db = Depends(get_db), device_id: Optional[str] = None):
    try:
        query = db.query(ReadDHT22)
        if device_id:
            query = query.filter(ReadDHT22.device_id == device_id)
        read = query.order_by(ReadDHT22.timestamp.desc()).first()
        return {k: v for k, v in read.__dict__.items() if k != "_sa_instance_state"} if read else {"error": "No readings found for this device"}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/average-reading")
#endpoint to retrieve average temperature and humidity for a specific device_id or all devices if no device_id is provided
def get_average_reading(db = Depends(get_db), device_id: Optional[str] = None, intervalo1: datetime = None, intervalo2: datetime = None):
    try:
        query = db.query(ReadDHT22)
        if not intervalo2:
            intervalo2 = datetime.now()
        if not intervalo1:
            intervalo1 = intervalo2 - timedelta(days=30)
        if device_id: 
            query = query.filter(ReadDHT22.device_id == device_id)
        query = query.filter(ReadDHT22.timestamp.between(intervalo1,intervalo2))
        avg_temp = query.with_entities(func.avg(ReadDHT22.temperature)).scalar()
        avg_humidity = query.with_entities(func.avg(ReadDHT22.humidity)).scalar()
        return {"average_temperature": avg_temp, "average_humidity": avg_humidity}
    except Exception as e:
        return {"error": str(e)}
