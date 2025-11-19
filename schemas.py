"""
Database Schemas for The Chess Club — The Observatory

Each Pydantic model corresponds to a MongoDB collection (lowercased class name).
Example: class Product -> collection name "product".
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime

# Community submissions (The Club)
class Submission(BaseModel):
    author_name: str = Field(..., description="Display name of the contributor")
    author_handle: Optional[str] = Field(None, description="Social or Chess.com handle")
    title: Optional[str] = Field(None, description="Optional title for the piece")
    content: Optional[str] = Field(None, description="Short text or caption")
    image_url: Optional[HttpUrl] = Field(None, description="Hosted image URL")
    tags: List[str] = Field(default_factory=list, description="Keywords or themes")

# Featured members (The Club)
class Member(BaseModel):
    name: str
    role: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    bio: Optional[str] = None

# Weekly thought (The Club)
class Thought(BaseModel):
    quote: str
    author: Optional[str] = None
    week_of: Optional[datetime] = None

# Archive entries (The Archive)
class ArchiveEntry(BaseModel):
    title: str
    subtitle: Optional[str] = None
    body: Optional[str] = None
    image_urls: List[HttpUrl] = Field(default_factory=list)
    timeline_label: Optional[str] = Field(None, description="e.g., S/S 24, Prototype v2")

# Events
class Event(BaseModel):
    title: str
    date: datetime
    location: str
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    rsvp_open: bool = True

class RSVP(BaseModel):
    event_id: str
    name: str
    email: str

# Shop
class Product(BaseModel):
    name: str
    slug: str = Field(..., description="URL-friendly identifier")
    price: float = Field(..., ge=0)
    currency: str = Field("USD")
    short: Optional[str] = Field(None, description="One-line story")
    description: Optional[str] = None
    images: List[HttpUrl] = Field(default_factory=list)
    in_stock: bool = True

# Newsletter
class NewsletterSignup(BaseModel):
    email: str
    source: Optional[str] = Field(None, description="e.g., hero-modal, footer")
