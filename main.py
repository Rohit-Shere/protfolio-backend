from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Enable CORS so your React frontend can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactPayload(BaseModel):
    sender_identity: str
    contact_ref: EmailStr
    payload_content: str

# Email Configuration (Use environment variables for security!)
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_USERNAME"),
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS= True,
    MAIL_SSL_TLS= True,
    USE_CREDENTIALS= True
)

@app.post("/establish-connection")
async def send_contact_email(payload: ContactPayload):
    message = MessageSchema(
        subject=f"PORTFOLIO_SIGNAL: {payload.sender_identity}",
        recipients=["rohitds6533@gmail.com"],
        body=f"""
        INBOUND_SIGNAL_DETECTED:
        -------------------------
        SENDER: {payload.sender_identity}
        REF: {payload.contact_ref}
        
        PAYLOAD:
        {payload.payload_content}
        """,
        subtype="plain"
    )
    
    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return {"status": "SUCCESS", "code": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))