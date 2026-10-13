import os, secrets
from contextlib import asynccontextmanager

from dotenv import load_dotenv


from fastapi import FastAPI, BackgroundTasks, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, EmailStr, Field

load_dotenv()

from email_service import send_email


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


API_KEY = os.getenv("API_KEY")
OWNER_EMAIL = os.getenv('OWNER_EMAIL')


app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "https://www.milanrawal.com.np"], allow_methods=["POST"], allow_headers=["*"])



class EmailRequest(BaseModel):
    sender_email: EmailStr
    subject: str = Field(max_length=120)
    body: str = Field(max_length=2000)


def verify(key: str | None = Header(None, alias="X-API-Key")):
    if not API_KEY or not key or not secrets.compare_digest(key, API_KEY):
        raise HTTPException(status_code=401, detail="Unauthorized")
    

    
@app.post('/send-email')
async def send_email_endpoint(
    request: EmailRequest,
    background_tasks: BackgroundTasks,
    _=Depends(verify)
):
    if not OWNER_EMAIL:
        raise HTTPException(status_code=500, detail="Server email not configured")
    background_tasks.add_task(
        send_email,
        recipient=OWNER_EMAIL,
        subject=request.subject,
        sender_email=str(request.sender_email),
        body=f"Question from: {request.sender_email}\n\n{request.body}"
    
    )
    
    return {"message": "Email notification scheduled"}