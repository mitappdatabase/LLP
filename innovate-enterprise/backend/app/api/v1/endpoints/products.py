"""
Product catalogue endpoints
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.product import Product, ProductImage
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
)
from app.core.security import get_current_user, check_permission

router = APIRouter()


@router.get("", response_model=ProductListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List all products with pagination and filtering"""
    
    # Build query
    query = db.query(Product)
    
    # Apply filters
    if category:
        query = query.filter(Product.category == category)
    
    if status:
        query = query.filter(Product.status == status)
    
    if search:
        query = query.filter(
            (Product.name.ilike(f"%{search}%")) |
            (Product.description.ilike(f"%{search}%"))
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    products = query.offset(offset).limit(page_size).all()
    
    return {
        "items": products,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Get a specific product by ID"""
    
    product = db.query(Product).filter(Product.product_id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new product (Admin only)"""
    
    # Check permission
    if not check_permission(current_user, "products", "create"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if product_id already exists
    existing = db.query(Product).filter(Product.product_id == product_data.product_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product ID already exists"
        )
    
    # Create product
    product = Product(
        product_id=product_data.product_id,
        name=product_data.name,
        category=product_data.category,
        description=product_data.description,
        specifications=product_data.specifications or {},
        features=product_data.features or [],
        applications=product_data.applications or [],
        status=product_data.status,
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    # Add images if provided
    if product_data.images:
        for idx, img_data in enumerate(product_data.images):
            image = ProductImage(
                product_id=product.id,
                image_url=img_data.image_url,
                display_order=img_data.display_order or idx,
                is_primary=img_data.is_primary,
            )
            db.add(image)
        db.commit()
    
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an existing product (Admin only)"""
    
    # Check permission
    if not check_permission(current_user, "products", "update"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    product = db.query(Product).filter(Product.product_id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Update fields
    update_data = product_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    return product


@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a product (Admin only)"""
    
    # Check permission
    if not check_permission(current_user, "products", "delete"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    product = db.query(Product).filter(Product.product_id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.delete(product)
    db.commit()
    
    return {"message": "Product deleted successfully"}


@router.get("/categories")
async def get_product_categories(
    db: Session = Depends(get_db),
):
    """Get all product categories"""
    
    categories = db.query(Product.category).distinct().all()
    return {"categories": [cat[0] for cat in categories]}
