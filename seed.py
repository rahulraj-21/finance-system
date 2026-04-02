from app.database import SessionLocal, engine
from app import models
from app.auth import hash_password
from datetime import date

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Create users
admin = models.User(email="admin@finance.com", hashed_password=hash_password("admin123"), role=models.RoleEnum.admin)
analyst = models.User(email="analyst@finance.com", hashed_password=hash_password("analyst123"), role=models.RoleEnum.analyst)
viewer = models.User(email="viewer@finance.com", hashed_password=hash_password("viewer123"), role=models.RoleEnum.viewer)

db.add_all([admin, analyst, viewer])
db.commit()
db.refresh(admin)

# Create transactions for admin
transactions = [
    models.Transaction(amount=5000, type="income", category="Salary", date=date(2026, 1, 1), notes="January salary", user_id=admin.id),
    models.Transaction(amount=1200, type="expense", category="Rent", date=date(2026, 1, 5), notes="Monthly rent", user_id=admin.id),
    models.Transaction(amount=300, type="expense", category="Food", date=date(2026, 1, 10), notes="Groceries", user_id=admin.id),
    models.Transaction(amount=5000, type="income", category="Salary", date=date(2026, 2, 1), notes="February salary", user_id=admin.id),
    models.Transaction(amount=1200, type="expense", category="Rent", date=date(2026, 2, 5), notes="Monthly rent", user_id=admin.id),
    models.Transaction(amount=150, type="expense", category="Transport", date=date(2026, 2, 15), notes="Bus pass", user_id=admin.id),
    models.Transaction(amount=500, type="income", category="Freelance", date=date(2026, 3, 1), notes="Project payment", user_id=admin.id),
    models.Transaction(amount=200, type="expense", category="Food", date=date(2026, 3, 8), notes="Restaurant", user_id=admin.id),
]

db.add_all(transactions)
db.commit()
db.close()

print("Database seeded successfully!")