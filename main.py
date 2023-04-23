import time
from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.database.db import get_db
from src.routes import contacts, auth
from src.services.email import conf


class EmailSchema(BaseModel):
    email: EmailStr


app = FastAPI()
favicon_path = 'favicon.ico'

@app.middleware('http')
async def custom_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    during = time.time() - start_time
    response.headers['performance'] = str(during)
    return response

templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

@app.get("/", response_class=HTMLResponse, description="Main Page")
async def root(request: Request):
    return templates.TemplateResponse('index.html', {"request": request, "title": "Contacts"})


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.post("/send-email")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=[body.email],
        template_body={"fullname": "Billy Jones"},
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message, template_name="example_email.html")

    return {"message": "email has been sent"}



app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)