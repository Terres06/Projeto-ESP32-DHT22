from fastapi import FastAPI
from db.schema import ReadDHT22, Session

app = FastAPI()

@app.get("/sensor-readings")

def get_sensor_readings(limit: int = 100, offset: int = 0):
    try:
        db = Session()
        read = db.query(ReadDHT22).offset(offset).limit(limit).all()
        return [{k: v for k, v in reading.__dict__.items() if k != "_sa_instance_state"} for reading in read]
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()