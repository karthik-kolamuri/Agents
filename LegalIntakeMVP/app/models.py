from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    email = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    contact = Column(String, index=True)
    matter_type = Column(String, nullable=True)
    jurisdiction = Column(String, nullable=True)
    urgency = Column(String, nullable=True)
    parties = Column(String, nullable=True) # Stored as comma-separated string or JSON
    created_at = Column(DateTime, default=datetime.utcnow)

    appointments = relationship("Appointment", back_populates="client")
    logs = relationship("InteractionLog", back_populates="client")

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    client_email = Column(String, ForeignKey("clients.email"))
    appointment_time = Column(DateTime)
    status = Column(String, default="Scheduled") # Scheduled, Completed, Cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="appointments")

class InteractionLog(Base):
    __tablename__ = "interaction_logs"

    id = Column(Integer, primary_key=True, index=True)
    client_email = Column(String, ForeignKey("clients.email"), nullable=True)
    action = Column(String) # e.g., "Consultation Booked", "Message Sent"
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="logs")
