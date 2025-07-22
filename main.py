from fastapi import FastAPI
from routes import case_routes, message_routes

app = FastAPI()

app.include_router(case_routes.router, prefix="/cases", tags=["cases"])
app.include_router(message_routes.router, prefix="/cases", tags=["messages"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Case Messaging API"}
