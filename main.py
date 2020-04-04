# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app.counter = 0

class PatientRq(BaseModel):
    name: str
    surename: str

class PatientResp(BaseModel):
    id: int
    patient: dict

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/method/")
def method_get():
    return {"method": "GET"}

@app.post("/method/")
def method_post():
    return {"method": "POST"}

@app.put("/method/")
def method_put():
    return {"method": "PUT"}

@app.delete("/method/")
def method_delete():
    return {"method": "DELETE"}

@app.post("/patient/", response_model=PatientResp)
def receive_patient(rq: PatientRq):
    app.counter += 1
    return PatientResp(id=app.counter,patient=rq.dict())
