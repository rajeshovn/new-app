from sqlalchemy.orm import Session
from ..models.audit_log import AuditLog
from datetime import datetime

def log_action(db: Session, user_id: int, action: str, ip_address: str):
    """
    Log user actions to the audit log
    
    Args:
        db (Session): Database session
        user_id (int): ID of the user performing the action
        action (str): Description of the action performed
        ip_address (str): IP address of the request
    """
    log_entry = AuditLog(
        user_id=user_id,
        action=action,
        ip_address=ip_address,
        timestamp=datetime.utcnow()
    )
    
    db.add(log_entry)
    db.commit()