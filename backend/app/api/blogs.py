"""Blogs API Routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.models import Blog, BlogStatus
from app.schemas import BlogResponse
router = APIRouter()

@router.get("/", response_model=list[BlogResponse])
async def list_blogs(
    category: Optional[str] = None,
    status: str = "published",
    db: Session = Depends(get_db)
):
    query = db.query(Blog).filter(Blog.status == BlogStatus.PUBLISHED)
    if category:
        query = query.filter(Blog.category_id == category)
    return query.all()

@router.get("/{slug}", response_model=BlogResponse)
async def get_blog(slug: str, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.slug == slug).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog
