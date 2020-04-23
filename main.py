from fastapi import FastAPI, Request, Query,  Cookie, HTTPException, Response, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse, RedirectResponse
#----------------------------
from typing import List
from hashlib import sha256
from fastapi.security import HTTPBasic, HTTPBasicCredentials
# main.py


app = FastAPI()
app.secret_key = "QXV0aG9yaXphdGlvbjogQmFzaWMgZEhKMVpHNVpPbEJoUXpFelRuUT0"
app.counter = 0
app.patients = []

security = HTTPBasic()

class PatientRq(BaseModel):
    name: str
    surename: str

class PatientResp(BaseModel):
    id: int
    patient: PatientRq

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
def root():
    return {"message": "Hello"}


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

#-------------------------------------------------------------------------------
@app.post("/login")
def create_cookie(credentials: HTTPBasicCredentials = Depends(security)):
    username = secrets.compare_digest(credentials.username,'trudnY')
    password = secrets.compare_digest(credentials.password, 'PaC13Nt')
    if not (username and password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect pass",
        )
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    print("session_token=",session_token)
    response.set_cookie(key="session_token", value=session_token)
    response = RedirectResponse(url='/welcome', status_code=HTTP_302_FOUND)
    return response
