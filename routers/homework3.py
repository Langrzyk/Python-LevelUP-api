import secrets
from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256

router = APIRouter()
security = HTTPBasic()

@router.get('/welcome')
@router.get('/')
def welcome():
    return {"message": "Welcome to my world!"}


@router.post("/login")
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
    response = RedirectResponse(url='/welcome', status_code=status.HTTP_302_FOUND)
