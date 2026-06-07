"""Projects API Routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.models import Project
from app.schemas import ProjectResponse
router = APIRouter()

@router.get("/", response_model=list[ProjectResponse])
async def list_projects(
    status: Optional[str] = None,
    featured: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(Project)
    if status:
        query = query.filter(Project.status == status)
    if featured:
        query = query.filter(Project.is_featured == True)
    return query.all()

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
