"""
Database Schemas for FocusFortress Prelaunch

Each Pydantic model represents a collection in MongoDB.
Class name lowercased is the collection name.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class EarlyAccessSignup(BaseModel):
    """Collect early access signups and plan selections"""
    email: EmailStr
    name: Optional[str] = Field(default=None)
    plan: str = Field(default="founder", description="selected early access plan")
    ref: Optional[str] = Field(default=None, description="referral/source tag")
    status: str = Field(default="registered")
