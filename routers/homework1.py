# main.py
from fastapi import Response, Request, APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from functools import wraps

router = APIRouter()
router.counter = 0
router.patients = []

class PatientRq(BaseModel):
    name: str
    surename: str

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

@router.post("/patient", response_model=PatientResp)
@to_authorize
def receive_patient(rq: PatientRq):
    app.patients.append(rq)
    app.counter += 1
    return PatientResp(id=app.counter,patient=rq)

@router.get("/patient/{pk}")
@to_authorize
def info_patient(pk: int):
    if pk < len(app.patients):
        return app.patients[pk]
    else:
        return JSONResponse(status_code=204)
