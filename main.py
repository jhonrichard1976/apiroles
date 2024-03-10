import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
from databases import Database
from typing import List, Optional
from fastapi import Path

DATABASE_URL = os.environ.get("PG_URL", "postgresql://postgres:1234@192.168.1.153/sigte_auth")
#DATABASE_URL = os.environ.get("PG_URL", "postgresql://adm_sigte_dev:sA7Egrm2jX@pgsqlqacl1.naiss.local/sigte_dev")
database = Database(DATABASE_URL)
metadata = MetaData()

# Define a new table with SQLAlchemy
roles = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("description", String(50)),
    Column("code", Integer),
    Column("status", Boolean),
)


# Define Pydantic models/schemas
class RolesIn(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[int] = None
    status: Optional[bool] = None


class Roles(BaseModel):
    id: int
    name: str
    description: str
    code: int
    status: bool


app = FastAPI()


# Event handlers to set up and close database connection
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Endpoints
@app.post("/roles/", response_model=Roles)
async def create_role(role: RolesIn):
    query = roles.insert().values(name=role.name, description=role.description, code=role.code, status=role.status)
    last_record_id = await database.execute(query)
    return {**role.dict(), "id": last_record_id}


@app.get("/roles/", response_model=List[Roles])
async def read_roles():
    query = roles.select()
    return await database.fetch_all(query)


@app.get("/roles/active", response_model=List[Roles])
async def read_active_roles():
    query = roles.select().where(roles.c.status == True)
    return await database.fetch_all(query)


@app.get("/roles/{role_id}", response_model=Roles)
async def read_role(role_id: int = Path(..., description="The ID of the role to get")):
    query = roles.select().where(roles.c.id == role_id)
    role = await database.fetch_one(query)
    if role is not None:
        return role
    raise HTTPException(status_code=404, detail=f"Role with id {role_id} not found")


@app.patch("/roles/{role_id}", response_model=Roles)
async def update_role(role_id: int, role: RolesIn):
    update_data = role.model_dump(exclude_unset=True)
    query = roles.update().where(roles.c.id == role_id).values(**update_data)
    await database.execute(query)

    # Recuperar y devolver la entidad actualizada
    query = roles.select().where(roles.c.id == role_id)
    updated_role = await database.fetch_one(query)
    if updated_role is not None:
        return updated_role
    raise HTTPException(status_code=404, detail=f"Role with id {role_id} not found")


@app.delete("/roles/{role_id}", response_model=Roles)
async def delete_role(role_id: int):
    query = roles.delete().where(roles.c.id == role_id)
    await database.execute(query)
    return {"message": f"Role with id {role_id} successfully deleted"}

# Add more endpoints as needed for CRUD operations
