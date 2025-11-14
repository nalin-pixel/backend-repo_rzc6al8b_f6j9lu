"""
Database Schemas for Specialty Coffee Ecommerce

Each Pydantic model represents a MongoDB collection. The collection name is the
lowercased class name (e.g., Product -> "product").
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

# Core domain
class Product(BaseModel):
    title: str = Field(..., description="Product title")
    slug: str = Field(..., description="URL-friendly slug")
    description: str = Field(..., description="Long description")
    price: float = Field(..., ge=0, description="Base price in USD")
    images: List[str] = Field(default_factory=list, description="Image URLs")
    roast_level: Literal["light", "medium", "dark"] = Field(..., description="Roast level")
    origin: Optional[str] = Field(None, description="Country/region of origin")
    flavor_notes: List[str] = Field(default_factory=list, description="Flavor notes")
    grind_options: List[str] = Field(default_factory=lambda: ["whole bean","espresso","filter","french press"]) 
    size_options: List[str] = Field(default_factory=lambda: ["250g","500g","1kg"])
    in_stock: bool = Field(True, description="Whether available for purchase")
    inventory: int = Field(100, ge=0, description="Units available (virtual stock)")
    rating: float = Field(4.8, ge=0, le=5, description="Average rating")
    tags: List[str] = Field(default_factory=list, description="Search/filter tags")

class Testimonial(BaseModel):
    name: str
    rating: int = Field(..., ge=1, le=5)
    comment: str
    photo_url: Optional[str] = None

class BlogPost(BaseModel):
    title: str
    slug: str
    excerpt: str
    content: str
    tags: List[str] = Field(default_factory=list)
    cover_image: Optional[str] = None

class User(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class OrderItem(BaseModel):
    product_id: str
    title: str
    size: str
    grind: str
    quantity: int = Field(..., ge=1)
    unit_price: float = Field(..., ge=0)

class Order(BaseModel):
    user_email: str
    items: List[OrderItem]
    subtotal: float
    shipping: float
    total: float
    status: Literal["pending","paid","shipped","delivered","cancelled"] = "paid"
    shipping_address: Optional[str] = None

class WholesaleInquiry(BaseModel):
    name: str
    business_name: str
    email: str
    phone: Optional[str] = None
    volume_needed: str
    message: Optional[str] = None

class ContactMessage(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    message: str

class NewsletterSubscription(BaseModel):
    email: str

# Note: These schemas are surfaced at GET /schema for admin tooling.
