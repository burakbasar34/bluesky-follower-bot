from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from views.routes import router
import os

app = FastAPI()

# Oturum yönetimi için middleware
app.add_middleware(SessionMiddleware, secret_key="supersecret")

# Statik dosyalar (CSS, JS vs.)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Tüm rotaları dahil et
app.include_router(router)
