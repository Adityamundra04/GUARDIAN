"""
SQLAlchemy ORM model for Incident database table.
Represents persistent storage of Kubernetes incidents.
"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from backend.app.core.database import Base
import uuid


class IncidentDB(Base):
    """
    SQLAlchemy ORM model for incidents table.
    
    Attributes:
        id: Unique identifier (UUID)
        issue: Description of the incident
        status: Current status (detected, resolved, etc.)
        cause: Root cause analysis
        solution: Proposed or applied solution
        action_taken: Action executed for remediation
        action_status: Status of the action
        created_at: Timestamp when incident was created
    """
    __tablename__ = "incidents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    issue = Column(String, nullable=False)
    status = Column(String, default="detected")
    cause = Column(String, nullable=True)
    solution = Column(String, nullable=True)
    action_taken = Column(String, nullable=True)
    action_status = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Incident(id={self.id}, issue={self.issue[:30]}..., status={self.status})>"
