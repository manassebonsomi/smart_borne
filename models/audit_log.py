from config.database import db
from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = "audit_log"

    id_audit = db.Column(
        db.Integer,
        primary_key=True
    )

    date_action = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    action = db.Column(
        db.String(255)
    )

    objet = db.Column(
        db.String(255)
    )

    resultat = db.Column(
        db.String(100)
    )

    details = db.Column(
        db.Text
    )