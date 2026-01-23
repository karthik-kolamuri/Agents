from app.database import SessionLocal, engine, Base
from app.models import Client, Appointment, InteractionLog
from sqlalchemy import text

def verify_db():
    print("--- 🔍 Verifying Database Connection & Schema ---")
    
    # Ensure tables are created
    print("⏳ Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    
    try:
        # Check connection
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✅ Database connection successful.")
        
        # Check if tables exist (basic check by querying empty)
        clients = db.query(Client).all()
        print(f"✅ Clients table exists. Count: {len(clients)}")
        
        appointments = db.query(Appointment).all()
        print(f"✅ Appointments table exists. Count: {len(appointments)}")
        
        logs = db.query(InteractionLog).all()
        print(f"✅ InteractionLogs table exists. Count: {len(logs)}")
        
        db.close()
        print("\n--- ✨ Database Verification Complete ---")
        return True
    except Exception as e:
        print(f"\n❌ Database Verification Failed: {e}")
        print("Tip: Make sure PostgreSQL is running and DATABASE_URL in .env is correct.")
        return False

if __name__ == "__main__":
    verify_db()
