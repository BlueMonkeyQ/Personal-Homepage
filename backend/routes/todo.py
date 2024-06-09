from typing import Any
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from database import supabase
from models.todo import Todo

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
    responses={404: {"message": "Not Found"}}
)

# ---------- GET ----------


# ---------- POST ----------


# ---------- PUT ----------


# ---------- DELETE ----------