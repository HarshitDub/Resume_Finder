# main_api.py

from fastapi import FastAPI
from routes.auth_routes import router as auth_router
from routes.scrape_routes import router as scrape_router
from routes.email_routes import router as email_router
from routes.export_routes import router as export_router

app = FastAPI(
    title="Resume Automation API",
    description="Modular backend API for scraping, emailing, exporting",
    version="1.0.0"
)

# Register all route modules
app.include_router(auth_router, prefix="/auth")
app.include_router(scrape_router, prefix="/scrape")
app.include_router(email_router, prefix="/email")
app.include_router(export_router, prefix="/export")
