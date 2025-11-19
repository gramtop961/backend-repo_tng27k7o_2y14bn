from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

from database import db, create_document, get_documents
from schemas import EarlyAccessSignup

app = FastAPI(title="FocusFortress API", version="1.0.0")

# Allow all origins for this pre-launch site
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SignupRequest(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    plan: Optional[str] = Field(default="founder", description="selected plan")
    ref: Optional[str] = Field(default=None, description="referral or source tag")


@app.get("/test")
async def test():
    status = {"api": "ok", "time": datetime.utcnow().isoformat() + "Z"}
    try:
        _ = db is not None
        status["db"] = "connected" if db is not None else "not_configured"
    except Exception:
        status["db"] = "error"
    return status


@app.post("/signup")
async def signup(payload: SignupRequest):
    try:
        doc = EarlyAccessSignup(
            email=str(payload.email),
            name=payload.name,
            plan=payload.plan,
            ref=payload.ref,
            status="registered",
        )
        doc_id = create_document("earlyaccesssignup", doc)
        return {"ok": True, "id": doc_id, "message": "You're on the list!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "FocusFortress API running"}
