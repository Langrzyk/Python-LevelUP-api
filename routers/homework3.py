import secrets
from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256

router = APIRouter()
security = HTTPBasic()
router.secret_key = "QXV0aG9yaXphdGlvbjogQmFzaWMgZEhKMVpHNVpPbEJoUXpFelRuUT0"

@router.get('/welcome')
@router.get('/')
def welcome():
    return {"message": "Welcome to my world!"}


@router.post("/login")
def create_cookie(credentials: HTTPBasicCredentials = Depends(security)):
    username_pass = secrets.compare_digest(credentials.username,'trudnY')
    password_pass = secrets.compare_digest(credentials.password, 'PaC13Nt')
    if not (username_pass and password_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect pass",
        )
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{router.secret_key}")).hexdigest()
    response.set_cookie(key="session_token", value=session_token)
    response = RedirectResponse(url='/welcome', status_code=status.HTTP_302_FOUND)
