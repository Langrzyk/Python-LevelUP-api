# main.py
from fastapi import APIRouter, Response, Request,
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router  = APIRouter()
router .counter = 0
router .patients = []

class PatientRq(BaseModel):
    name: str
    surename: str

class PatientResp(BaseModel):
    id: int
    patient: PatientRq

# @router.get("/")
# def root():
#     return {"message": "Hello World during the coronavirus pandemic!"}

@router.get("/method")
def method_get():
    return {"method": "GET"}

@router.post("/method")
def method_post():
    return {"method": "POST"}

@router.put("/method")
def method_put():
    return {"method": "PUT"}

@router.delete("/method/")
def method_delete():
    return {"method": "DELETE"}

@router.post("/patient", response_model=PatientResp)
def receive_patient(rq: PatientRq):
    app.patients.append(rq)
    app.counter += 1
    return PatientResp(id=app.counter,patient=rq)

@router.get("/patient/{pk}")
def info_patient(pk: int):
    if pk < len(app.patients):
        return app.patients[pk]
    else:
        return JSONResponse(status_code=204)
