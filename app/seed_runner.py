from app.db import Base, engine, SessionLocal
from app.seed import run_seed

def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        run_seed(db)
        print("✅ Seed completed")
    finally:
        db.close()

if __name__ == "__main__":
    main()
