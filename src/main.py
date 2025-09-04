from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .appointment.routes import router as appointment_router
from .auth.routes import router
from .pharmacy.routes import router as pharmacy_router
from .asha_worker.routes import router as asha_worker_router


app = FastAPI()

# CORS for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/auth", tags=["Authentication"])
app.include_router(appointment_router, prefix="/appointments", tags=["Appointments"])
app.include_router(pharmacy_router, prefix="/pharmacies", tags=["Pharmacies"])
app.include_router(asha_worker_router, prefix="/asha_worker", tags=["ASHA Worker"])
