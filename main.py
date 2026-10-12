from contextlib import asynccontextmanager

from dotenv import load_dotenv


from fastapi import FastAPI, UploadFile, File, BackgroundTasks

from pydantic import BaseModel, EmailStr

load_dotenv()

from email_service import send_email


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


class EmailRequest(BaseModel):
    sender_email: EmailStr
    recipient: EmailStr
    subject: str
    body: str


    
@app.post('/send-email')
async def send_email_endpoint(
    request: EmailRequest,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(
        send_email,
        recipient = str(request.recipient),
        subject=request.subject,
        sender_email=str(request.sender_email),
        body=f"Question from: {request.sender_email}\n\n{request.body}"
    
    )
    
    return {"message": "Email notification scheduled"}