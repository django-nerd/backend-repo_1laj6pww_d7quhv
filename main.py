import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson.objectid import ObjectId

from database import db, create_document, get_documents
from schemas import Submission, Member, Thought, ArchiveEntry, Event, RSVP, Product, NewsletterSignup

app = FastAPI(title="The Chess Club — The Observatory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"name": "The Chess Club — The Observatory API", "status": "ok"}

# Utility to convert Mongo _id to string

def serialize(doc):
    if not doc:
        return doc
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc

# ---------- The Club (Community) ----------

@app.post("/api/submissions")
def create_submission(item: Submission):
    _id = create_document("submission", item)
    return {"id": _id}

@app.get("/api/submissions")
def list_submissions(limit: int = 24):
    docs = get_documents("submission", {}, limit)
    return [serialize(d) for d in docs]

@app.post("/api/members")
def create_member(item: Member):
    _id = create_document("member", item)
    return {"id": _id}

@app.get("/api/members")
def list_members(limit: int = 12):
    docs = get_documents("member", {}, limit)
    return [serialize(d) for d in docs]

@app.post("/api/thought")
def set_thought(item: Thought):
    _id = create_document("thought", item)
    return {"id": _id}

@app.get("/api/thought")
def get_thought():
    docs = get_documents("thought", {}, 1)
    return serialize(docs[-1]) if docs else None

# ---------- Archive ----------

@app.post("/api/archive")
def create_archive(item: ArchiveEntry):
    _id = create_document("archiveentry", item)
    return {"id": _id}

@app.get("/api/archive")
def list_archive(limit: int = 20):
    docs = get_documents("archiveentry", {}, limit)
    return [serialize(d) for d in docs]

# ---------- Events ----------

@app.post("/api/events")
def create_event(item: Event):
    _id = create_document("event", item)
    return {"id": _id}

@app.get("/api/events")
def list_events(limit: int = 20):
    docs = get_documents("event", {}, limit)
    return [serialize(d) for d in docs]

@app.post("/api/rsvp")
def create_rsvp(item: RSVP):
    _id = create_document("rsvp", item)
    return {"id": _id}

# ---------- Shop ----------

@app.post("/api/products")
def create_product(item: Product):
    _id = create_document("product", item)
    return {"id": _id}

@app.get("/api/products")
def list_products(limit: int = 24):
    docs = get_documents("product", {}, limit)
    return [serialize(d) for d in docs]

@app.get("/api/products/{slug}")
def get_product(slug: str):
    docs = get_documents("product", {"slug": slug}, 1)
    if not docs:
        raise HTTPException(status_code=404, detail="Product not found")
    return serialize(docs[0])

# ---------- Newsletter ----------

@app.post("/api/newsletter")
def newsletter_signup(item: NewsletterSignup):
    _id = create_document("newslettersignup", item)
    return {"id": _id}

# ---------- Health / Test ----------

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
