from app.database import engine, Base
from sqlalchemy import text

def reset_db():
    print("--- 🗑️  Resetting Database Schema ---")
    connection = engine.connect()
    # Drop tables with CASCADE to ensure everything goes
    print("Dropping interaction_logs...")
    connection.execute(text("DROP TABLE IF EXISTS interaction_logs CASCADE"))
    print("Dropping appointments...")
    connection.execute(text("DROP TABLE IF EXISTS appointments CASCADE"))
    print("Dropping clients...")
    connection.execute(text("DROP TABLE IF EXISTS clients CASCADE"))
    connection.commit()
    connection.close()
    print("✅ Tables dropped. They will be recreated on next run.")

if __name__ == "__main__":
    reset_db()
