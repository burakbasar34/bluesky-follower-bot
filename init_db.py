from database import engine, Base
from models import User, TargetUser, FollowLog

def init():
    print("Veritabanı ve tablolar oluşturuluyor...")
    Base.metadata.create_all(bind=engine)
    print("Tamamlandı.")

if __name__ == "__main__":
    init()
