from fastapi import FastAPI
from .routers import auth, supplier



app=FastAPI()
app.include_router(auth.router)
app.include_router(supplier.router)

@app.get("/")
async def root():   
    return {"message": "Welcome to the Companies Management API!"}