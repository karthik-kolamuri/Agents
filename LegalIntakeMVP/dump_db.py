from app.database import SessionLocal
from app.models import Client, Appointment, InteractionLog

def dump_db():
    db = SessionLocal()
    
    print("\n--- 👥 Clients ---")
    clients = db.query(Client).all()
    for c in clients:
        print(f"Email: {c.email} | Name: {c.name} | Contact: {c.contact} | Matter: {c.matter_type}")
        
    print("\n--- 📅 Appointments ---")
    appts = db.query(Appointment).all()
    for a in appts:
        print(f"ID: {a.id} | ClientEmail: {a.client_email} | Time: {a.appointment_time} | Status: {a.status}")

    print("\n--- 📜 Logs ---")
    logs = db.query(InteractionLog).all()
    for l in logs:
        print(f"ID: {l.id} | ClientEmail: {l.client_email} | Action: {l.action} | Details: {l.details}")

    db.close()

if __name__ == "__main__":
    dump_db()
