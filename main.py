import datetime as dt
from datetime import datetime, timedelta
import json
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from modules.event.routes import event_router
from modules.db.routes import db_router
from modules.auth.auth import login_for_access_token


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(db_router)
app.include_router(event_router)


@app.post("/login")
async def login_for_access_token_(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await login_for_access_token(form_data)
    return result

