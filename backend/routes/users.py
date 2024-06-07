from typing import Any
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from database import supabase
from models.users import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"message": "Not Found"}}
)

# ---------- GET ----------

# Gets all users
@router.get("")
def get_users() -> Any:
    try:
        users = supabase.from_("users")\
        .select("id, username, firstname, lastname")\
        .order(column="id", desc=False)\
        .execute().data

        return users

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET user, error: {str(e)}")

# Gets user via id
@router.get("/{id}")
def get_user(id):
    try:
        user = supabase.from_("users")\
        .select("*")\
        .eq(column="id", value=id)\
        .limit(size=1)\
        .execute().data[0]

        if user:
            return user

        return HTTPException(status_code=400, detail="User not found")

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET user, error: {str(e)}")


# ---------- POST ----------
@router.post("")
def create_user(user: User):
    try:
        supabase.from_("users")\
        .insert({
            "username": user.username.lower(),
            "password": user.password,
            "firstname": user.firstname,
            "lastname": user.lastname,
        })\
        .execute()

        user_id = supabase.from_("users")\
            .select("id")\
            .limit(size=1)\
            .order(column="id", desc=True)\
            .execute().data[0]
        
        return JSONResponse(status_code=201, content=user_id)
    
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to POST user, error: {str(e)}")

# ---------- PUT ----------
@router.put("/{id}")
def update_user(id: int, user_in: User):
    try:
        user = supabase.from_("users")\
        .select("id")\
        .eq(column="id", value=id)\
        .limit(size=1)\
        .execute().data

        if len(user) != 0:
            supabase.from_("users")\
            .update({
                "username": user_in.username.lower(),
                'password': user_in.password,
                'firstname': user_in.firstname,
                'lastname': user_in.lastname
            })\
            .eq(column='id', value=id)\
            .execute()

            return JSONResponse(status_code=200, content={'message':True})

        else:
            return HTTPException(status_code=404, detail=f"Unable to Find User with id: {id}")

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to UPDATE User, error: {str(e)}")
    
# ---------- DELETE ----------
@router.delete("/{id}")
def delete_user(id: int):
    try:
        user = supabase.from_("users")\
        .select("id")\
        .eq(column="id", value=id)\
        .limit(size=1)\
        .execute().data

        if len(user) != 0:
            supabase.from_("users")\
            .delete()\
            .eq(column='id', value=id)\
            .execute()

            return JSONResponse(status_code=200, content={'message':True})

        else:
            return HTTPException(status_code=404, detail=f"Unable to Find User with id: {id}")

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to DELETE User, error: {str(e)}")