from src.db import Base, engine

# Import all models here
from src.auth.models import User
from src.appointment.models import Appointment
from src.pharmacy.models import Pharmacy, Medicine
from src.profiles.models import Patient, Doctor, Pharmacist, ASHAWorker
from src.prescriptions.models import Prescription

print("Dropping all database tables...")
# This command will drop all tables known to Base
Base.metadata.drop_all(bind=engine)
print("Tables dropped.")

print("Creating all database tables...")
# This command creates all tables
Base.metadata.create_all(bind=engine)
print("All tables created successfully.")