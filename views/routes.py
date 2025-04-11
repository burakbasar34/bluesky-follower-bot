from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, TargetUser, FollowLog
from services.follow import follow_likers
from starlette.status import HTTP_302_FOUND
from datetime import date

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(request: Request, username: str = Form(...), app_password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(username=username, app_password=app_password)
        db.add(user)
        db.commit()
        db.refresh(user)
    request.session["user_id"] = user.id
    return RedirectResponse(url="/dashboard", status_code=HTTP_302_FOUND)

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/", status_code=HTTP_302_FOUND)
    user = db.query(User).get(user_id)
    logs = db.query(FollowLog).filter(FollowLog.user_id == user_id).order_by(FollowLog.created_at.desc()).limit(20).all()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "targets": user.targets,
        "logs": logs
    })

@router.post("/add-target")
def add_target(request: Request, handle: str = Form(...), db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if user_id:
        target = TargetUser(handle=handle.lstrip("@"), user_id=user_id)
        db.add(target)
        db.commit()
    return RedirectResponse(url="/dashboard", status_code=HTTP_302_FOUND)

@router.post("/follow-likers")
def follow_likers_manual(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    user = db.query(User).get(user_id)
    follow_likers(db, user)
    return RedirectResponse(url="/dashboard", status_code=HTTP_302_FOUND)

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=HTTP_302_FOUND)
