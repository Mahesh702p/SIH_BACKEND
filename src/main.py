from fastapi import FastAPI
from .appointment.routes import router as appointment_router
from .auth.routes import router
from .pharmacy.routes import router as pharmacy_router

app = FastAPI()

app.include_router(router, prefix="/auth", tags=["Authentication"])
app.include_router(appointment_router, prefix="/appointments", tags=["Appointments"])
app.include_router(pharmacy_router, prefix="/pharmacies", tags=["Pharmacies"])
