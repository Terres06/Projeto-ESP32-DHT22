from typing import Optional
from fastapi import FastAPI, Depends
from db.schema import ReadDHT22, Session

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