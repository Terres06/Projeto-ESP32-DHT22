from typing import Optional
from fastapi import FastAPI
from db.schema import ReadDHT22, Session

app = FastAPI()

@app.get("/sensor-readings")

#endpoint to retrieve all sensor readings with pagination and optional device_id filter
def get_sensor_readings(limit: int = 100, offset: int = 0,device_id: Optional[str] = None):
    try:
        db = Session()
        query = db.query(ReadDHT22)
        if device_id:
            query = query.filter(ReadDHT22.device_id == device_id)
        read = query.offset(offset).limit(limit).all()
        return [{k: v for k, v in reading.__dict__.items() if k != "_sa_instance_state"} for reading in read]
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

@app.get("/last-reading")

#endpoint to retrieve the last sensor reading for a specific device_id or the most recent reading if no device_id is provided
def get_last_reading(device_id: Optional[str] = None):
    try:
        db = Session()
        query = db.query(ReadDHT22)
        if device_id:
            query = query.filter(ReadDHT22.device_id == device_id)
        read = query.order_by(ReadDHT22.timestamp.desc()).first()
        return {k: v for k, v in read.__dict__.items() if k != "_sa_instance_state"} if read else {"error": "No readings found for this device"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()