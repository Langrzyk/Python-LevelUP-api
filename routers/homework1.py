# main.py
from fastapi import Response, Request, APIRouter, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse, RedirectResponse
from functools import wraps

router = APIRouter()
router.counter = 0
patients = {}

class PatientRq(BaseModel):
    name: str
    surname: str

class PatientResp(BaseModel):
    id: int
    patient: PatientRq

#dekorator
def to_authorize(to_authorize):
    @wraps(to_authorize)
    def inner(request: Request, *args, **kwargs):
        if request.cookies.get('session_token'):
            result = to_authorize(request, *args, **kwargs)
        else:
             result = RedirectResponse(url='/', status_code=status.HTTP_401_UNAUTHORIZED)
        return result
    return inner


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

@router.post("/patient")
@to_authorize
def patient_POST(request: Request, new_patient: PatientRq):
    global patients
    if len(patients.keys()) == 0:
        id = 0
    else:
        id = max(patients.keys()) + 1
    patients[id] = new_patient

    return RedirectResponse(url=f'/patient/{id}', status_code=status.HTTP_302_FOUND)

@router.get("/patient")
@to_authorize
def patient_GET(request: Request):
    return patients


@router.get("/patient/{pk}")
@to_authorize
def info_patient(request: Request, pk: int):
    if pk in patients.keys():
        return patients[pk]
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/patient/{pk}")
@to_authorize
def patient_DELETE(request: Request, pk: int):
    if pk in patients.keys():
        del patients[pk]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
