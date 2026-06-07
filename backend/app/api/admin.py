"""Admin API Routes - Dashboard & Management"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import User, Product, Project, Blog, Contact, Farmer, SupportTicket
from app.schemas import DashboardMetrics
from app.utils.security import get_current_superuser

router = APIRouter()

@router.get("/dashboard", response_model=DashboardMetrics)
async def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    return DashboardMetrics(
        total_visitors=0,
        total_leads=db.query(Contact).count(),
        total_products=db.query(Product).count(),
        total_projects=db.query(Project).count(),
        total_blogs=db.query(Blog).count(),
        total_contacts=db.query(Contact).count(),
        total_farmers=db.query(Farmer).count(),
        pending_tickets=db.query(SupportTicket).filter(SupportTicket.status == "open").count(),
        recent_applications=0
    )
