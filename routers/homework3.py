import secrets
from fastapi import APIRouter, Request, Query,  Cookie, HTTPException, Response, Depends,status
from pydantic import BaseModel
from fastapi.responses import JSONResponse, RedirectResponse
#----------------------------
from typing import List
from hashlib import sha256
from fastapi.security import HTTPBasic, HTTPBasicCredentials
# main.py


router  = APIRouter()
app.secret_key = "QXV0aG9yaXphdGlvbjogQmFzaWMgZEhKMVpHNVpPbEJoUXpFelRuUT0"

security = HTTPBasic()

@router.get("/welcome")
@router.get('/')
def root():
    return {"message": "Hello"}


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
