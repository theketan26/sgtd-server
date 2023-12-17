import datetime as dt
from datetime import datetime, timedelta
import json
from fastapi import FastAPI, Depends, HTTPException, status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from modules.event.routes import event_router
from modules.db.routes import db_router
from modules.auth.auth import get_current_user, login_for_access_token


app = FastAPI()
app.include_router(db_router)
app.include_router(event_router)


@app.post("/login")
async def login_for_access_token_(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await login_for_access_token(form_data)
    return result

