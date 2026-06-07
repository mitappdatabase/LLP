"""
Authentication API Routes
Handles user registration, login, token management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models import User, RefreshToken, UserRole
from app.schemas import (
    UserCreate, UserResponse, LoginRequest, TokenResponse,
    ChangePasswordRequest, RefreshTokenRequest, ResponseBase
)
from app.utils.security import (
    verify_password, get_password_hash, create_access_token,
    get_current_user, get_current_active_user, decode_token,
    get_client_ip
)

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    
    - **email**: Valid email address
    - **username**: Unique username (3-100 characters)
    - **password**: Password (minimum 8 characters)
    - **full_name**: Optional full name
    """
    # Check if email already exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=UserRole.VIEWER,  # Default role
        is_active=True,
        is_verified=False,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    """
    Authenticate user and return access tokens.
    
    - **username**: Username or email
    - **password**: User password
    
    Returns access token and refresh token for authentication.
    """
    # Find user by username or email
    user = db.query(User).filter(
        (User.username == login_data.username) | (User.email == login_data.username)
    ).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id), "type": "access"}
    )
    
    # Create refresh token
    refresh_token_data = create_refresh_token(
        user_id=user.id,
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("user-agent")
    )
    
    # Store refresh token in database
    db_refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token_data,
        expires_at=datetime.utcnow() + timedelta(days=7),
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("user-agent")
    )
    db.add(db_refresh_token)
    db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_data,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Valid refresh token
    """
    # Find refresh token in database
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == token_data.refresh_token
    ).first()
    
    if not db_token or db_token.is_revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked refresh token"
        )
    
    if db_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )
    
    # Get user
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new access token
    access_token = create_access_token(
        data={"sub": str(user.id), "type": "access"}
    )
    
    # Create new refresh token
    new_refresh_token = create_refresh_token(user_id=user.id)
    
    # Revoke old refresh token
    db_token.is_revoked = True
    
    # Store new refresh token
    db_new_token = RefreshToken(
        user_id=user.id,
        token=new_refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(db_new_token)
    db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/logout")
async def logout(
    token_data: RefreshTokenRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Logout user by revoking refresh token.
    
    Invalidates the provided refresh token.
    """
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == token_data.refresh_token,
        RefreshToken.user_id == current_user.id
    ).first()
    
    if db_token:
        db_token.is_revoked = True
        db.commit()
    
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user information.
    
    Requires valid access token in Authorization header.
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile.
    
    Can update email, username, and full_name.
    """
    update_data = {k: v for k, v in user_update.items() if v is not None}
    
    # Check email uniqueness if changing email
    if "email" in update_data and update_data["email"] != current_user.email:
        existing = db.query(User).filter(User.email == update_data["email"]).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
    
    # Check username uniqueness if changing username
    if "username" in update_data and update_data["username"] != current_user.username:
        existing = db.query(User).filter(User.username == update_data["username"]).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already in use"
            )
    
    # Update user
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.post("/change-password")
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Change user password.
    
    - **current_password**: Current password
    - **new_password**: New password (minimum 8 characters)
    """
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Update password
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}


# Import settings for expires_in calculation
from app.core.config import settings
