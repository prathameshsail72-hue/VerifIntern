import uvicorn
from fastapi import FastAPI

from api import report, search
from config.database import Base, engine

# Automatically create the SQLite database file and tables on run
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VerifIntern Platform Core Engine",
    description="Automated structural micro-service validating recruiter trust metrics.",
    version="1.0.0",
)

# Connect modular sub-routers
app.include_router(search.router)
app.include_router(report.router)


@app.get("/")
def home():
    return {"message": "VerifIntern Core API is running perfectly."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)