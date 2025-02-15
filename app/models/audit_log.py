from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..utils.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(255))
    ip_address = Column(String(45))
    timestamp = Column(DateTime)

    # Relationship with User model (optional)
    user = relationship("User", back_populates="audit_logs")