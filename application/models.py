import random
from app import db
from datetime import datetime
import uuid


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Staff(TimestampMixin, db.Model):
    __tablename__ = 'staff'

    # Internal unique identifier (Primary Key)
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Human-friendly staff ID
    staffID = db.Column(db.String(6), unique=True, nullable=False, default=lambda: generate_staff_id())

    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default='staff')  # 'staff' or 'admin'
    lineManagerID = db.Column(db.String, db.ForeignKey('staff.id'), nullable=True)

    # Leave balances stored as JSON
    leaveBalances = db.Column(db.JSON, default={
        'sick_leave': 10,
        'exam_leave': 5,
        'annual_leave': 20,
        'compassionate_leave': 0,
    })

    # Relationships
    requests = db.relationship('LeaveRequest', backref='staff', lazy=True, foreign_keys="LeaveRequest.staff_id")
    managed_requests = db.relationship('LeaveRequest', backref='line_manager', lazy=True, foreign_keys="LeaveRequest.line_manager_id")


# Utility function to generate unique 6-digit staff IDs
def generate_staff_id():
    while True:
        staff_id = str(random.randint(100000, 999999))
        if not Staff.query.filter_by(staffID=staff_id).first():
            return staff_id


class LeaveRequest(TimestampMixin, db.Model):
    __tablename__ = 'leave_request'

    # Internal unique identifier (Primary Key)
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))

    type = db.Column(db.String, nullable=False)  # 'sick_leave', 'exam_leave', etc.
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    resumptionDate = db.Column(db.Date, nullable=False)
    status = db.Column(db.String, default='pending')  # 'pending', 'approved', 'rejected'
    dateRequested = db.Column(db.DateTime, default=datetime.utcnow)
    dateApproved = db.Column(db.DateTime, nullable=True)
    initialBalance = db.Column(db.Integer, nullable=False)
    finalBalance = db.Column(db.Integer, nullable=True)

    # Foreign Keys
    staff_id = db.Column(db.String, db.ForeignKey('staff.id'), nullable=False)
    line_manager_id = db.Column(db.String, db.ForeignKey('staff.id'), nullable=False)


class AuditLog(TimestampMixin, db.Model):
    __tablename__ = 'audit_log'

    # Internal unique identifier (Primary Key)
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String, nullable=False)  # e.g., "Created Leave Request"
    details = db.Column(db.Text, nullable=True)

    # Foreign Key
    performed_by = db.Column(db.String, db.ForeignKey('staff.id'), nullable=False)

    # Relationships
    staff = db.relationship('Staff', backref='audit_logs')
