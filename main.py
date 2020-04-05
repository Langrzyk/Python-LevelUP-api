# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()
app.counter = 0
app.patients = []

class PatientRq(BaseModel):
    name: str
    surename: str

class PatientResp(BaseModel):
    id: int
    patient: PatientRq

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/method")
def method_get():
    return {"method": "GET"}

@app.post("/method")
def method_post():
    return {"method": "POST"}

@app.put("/method")
def method_put():
    return {"method": "PUT"}

@app.delete("/method/")
def method_delete():
    return {"method": "DELETE"}

@app.post("/patient", response_model=PatientResp)
def receive_patient(rq: PatientRq):
    app.patients.append(rq)
    app.counter += 1
    return PatientResp(id=app.counter,patient=rq)

@app.get("/patient/{pk}")
def info_patient(pk: int):
    if pk < len(app.patients):
        return app.patients[pk]
    else:
        return JSONResponse(status_code=204)
