from fastapi import FastAPI
from .routers import products, auth, supplier, companies, users, roles
app=FastAPI()

app.include_router(users.router)
app.include_router(companies.router)
app.include_router(auth.router)
app.include_router(supplier.router)
app.include_router(roles.router)
app.include_router(products.router)

@app.get("/")
async def root():   
    return {"message": "Welcome to the Companies Management API!"}