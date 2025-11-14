import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Product, Testimonial, BlogPost, Order, WholesaleInquiry, ContactMessage, NewsletterSubscription

app = FastAPI(title="Specialty Coffee API", description="Ecommerce backend for a specialty coffee brand")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Specialty Coffee API running"}

# Public catalog endpoints
@app.get("/api/products", response_model=List[Product])
def list_products():
    items = get_documents("product")
    for it in items:
        it.pop("_id", None)
    return items

@app.get("/api/products/{slug}", response_model=Product)
def get_product(slug: str):
    items = get_documents("product", {"slug": slug}, limit=1)
    if not items:
        raise HTTPException(404, "Product not found")
    doc = items[0]
    doc.pop("_id", None)
    return doc

@app.get("/api/testimonials", response_model=List[Testimonial])
def list_testimonials():
    items = get_documents("testimonial")
    for it in items:
        it.pop("_id", None)
    return items

@app.get("/api/blog", response_model=List[BlogPost])
def list_blog():
    posts = get_documents("blogpost")
    for p in posts:
        p.pop("_id", None)
    return posts

@app.get("/api/blog/{slug}", response_model=BlogPost)
def get_blog(slug: str):
    posts = get_documents("blogpost", {"slug": slug}, limit=1)
    if not posts:
        raise HTTPException(404, "Post not found")
    doc = posts[0]
    doc.pop("_id", None)
    return doc

# Forms & ecommerce flows (simplified for demo)
@app.post("/api/wholesale")
def submit_wholesale(data: WholesaleInquiry):
    create_document("wholesaleinquiry", data)
    return {"ok": True}

@app.post("/api/contact")
def submit_contact(data: ContactMessage):
    create_document("contactmessage", data)
    return {"ok": True}

@app.post("/api/subscribe")
def subscribe(data: NewsletterSubscription):
    create_document("newslettersubscription", data)
    return {"ok": True}

# Checkout simulation (no real payment in this environment)
class CheckoutPayload(BaseModel):
    order: Order

@app.post("/api/checkout")
def checkout(payload: CheckoutPayload):
    order_id = create_document("order", payload.order)
    return {"ok": True, "order_id": order_id}

# Admin endpoints (simple)
@app.post("/api/admin/product")
def admin_create_product(product: Product):
    create_document("product", product)
    return {"ok": True}

@app.get("/schema")
def get_schema():
    # For Flames database viewer
    from inspect import getsource
    import schemas as schemas_module
    return {"schemas": getsource(schemas_module)}

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
            response["database_name"] = getattr(db, 'name', '✅ Connected')
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
