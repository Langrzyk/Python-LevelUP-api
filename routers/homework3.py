import secrets
from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256
from functools import wraps
from fastapi.templating import Jinja2Templates

router = APIRouter()
security = HTTPBasic()
templates = Jinja2Templates(directory="templates")
router.secret_key = "QXV0aG9yaXphdGlvbiBCYXNpYyBsb2dpbjogdHJ1ZG5ZIHBhc3N3b3JkOiBQYUMx"

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

@router.get('/')
def root():
    return {"message": "Welcome to my world!"}

@router.get('/welcome')
@to_authorize
def welcome(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request, "user": "trudnY"})


@router.post("/login")
def create_cookie(credentials: HTTPBasicCredentials = Depends(security)):
    username_pass = secrets.compare_digest(credentials.username,'trudnY')
    password_pass = secrets.compare_digest(credentials.password,'PaC13Nt')
    if not (username_pass and password_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect pass",
        )
    session_token = sha256(str.encode(f"{credentials.username}{credentials.password}{router.secret_key}")).hexdigest()
    response = RedirectResponse(url='/welcome', status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="session_token", value=session_token)
    return response

@router.post("/login")
@to_authorize
def logout(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("session_token")
    return response
