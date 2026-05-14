from fastapi import FastAPI

from app.routes.claims import (
    router as claims_router
)

app = FastAPI(
    title="Insurance Claims Agent"
)

app.include_router(
    claims_router
)


@app.get("/")
def root():

    return {
        "message": "Insurance Claims Agent Running"
    }