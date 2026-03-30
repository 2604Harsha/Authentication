from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.v1.routers import users
from utils.dependencies import engine
from core.database import Base
from fastapi.middleware.cors import CORSMiddleware
from models.user import User
from models.email_token import EmailToken
from models.token_blacklist import TokenBlacklist

from api.v1.routers import auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/forgot-password")
def forgot_page(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

@app.get("/reset-password")
def reset_page(request: Request):
    return templates.TemplateResponse("reset_password.html", {"request": request})

@app.get("/verify")
def verify_email_page(request: Request):
    """
    This page is opened when user clicks verification link from email
    """
    return templates.TemplateResponse("verify.html", {"request": request})



@app.get("/login-otp")
async def login_otp_page(request: Request):
    return templates.TemplateResponse(
        "login_otp.html",
        {"request": request}
    )

@app.get("/password")
def forgot_page(request: Request):
    return templates.TemplateResponse("password.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


@app.get("/profile")
def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})


@app.get("/security")
def security(request: Request):
    return templates.TemplateResponse("security.html", {"request": request})

@app.get("/activity")
def activity_page(request: Request):
    return templates.TemplateResponse("activity.html", {"request": request})

@app.get("/settings")
def activity_page(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})