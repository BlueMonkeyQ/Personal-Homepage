import pandas as pd
from typing import Any
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from database import supabase
from datetime import datetime
from models.fitness import Exercise, Sets, Workouts

router = APIRouter(
    prefix="/fitness",
    tags=["Fitness"],
    responses={404: {"message": "Not Found"}}
)

# ---------- GET ----------
@router.get("/workouts", tags=['Fitness'])
def get_workouts(uid: int, date: str):
    try:
        workouts = supabase.from_("workouts")\
        .select("*")\
        .eq(column="uid", value=uid)\
        .eq(column="date", value=date)\
        .execute().data

        return JSONResponse(status_code=200, content=workouts)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET workouts, error: {str(e)}")
    

@router.get("/workouts/{id}", tags=['Fitness'])
def get_workout(id: int):
    try:
        workout = supabase.from_("workouts")\
        .select("*")\
        .eq(column="id", value=id)\
        .execute().data[0]

        return JSONResponse(status_code=200, content=workout)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET workout, error: {str(e)}")
    

@router.get("/sets/{id}", tags=['Fitness'])
def get_set(id: int):
    try:
        _set = supabase.from_("sets")\
        .select("*")\
        .eq(column="id", value=id)\
        .execute().data[0]

        return JSONResponse(status_code=200, content=_set)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET set, error: {str(e)}")

@router.get("/exercises/names", tags=['Fitness'])
def get_exercises_names():
    try:
        exercises = supabase.from_("exercises")\
        .select("id, name")\
        .execute().data

        return JSONResponse(status_code=200, content=exercises)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET exercises, error: {str(e)}")

@router.get("/exercises/{id}", tags=['Fitness'])
def get_exercise(id: int):
    try:
        exercise = supabase.from_("exercises")\
        .select("*")\
        .eq(column="id", value=id)\
        .execute().data[0]

        return JSONResponse(status_code=200, content=exercise)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET exercise, error: {str(e)}")
    

# ---------- POST ----------
# @TODO: standardize date
@router.post("/workouts", tags=['Fitness'])
def add_workout_set(workout: Workouts):
    try:
        # Insert Set and return the sid
        supabase.from_("sets")\
        .insert({
            "reps": workout.reps,
            "weight": workout.weight
        })\
        .execute()

        workout.sid = supabase.from_("sets")\
        .select("id")\
        .order(column="id", desc=True)\
        .limit(size=1)\
        .execute().data[0]["id"]

        print(workout.sid)

        # Insert Workout
        supabase.from_("workouts")\
        .insert({
            "uid": workout.uid,
            "eid": workout.eid,
            "sid": workout.sid,
            "date": workout.date
        })\
        .execute()

        return JSONResponse(status_code=201, content={
            "uid": workout.uid,
            "eid": workout.eid,
            "sid": workout.sid,
            "date": workout.date
        })

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to POST workout, error: {str(e)}")
    
@router.post("/exercises/generate", tags=['Fitness'])
def generate_exercise():
    try:
        df = pd.read_csv(r"data/exercises.csv")
        df.fillna(value="None", inplace=True)

        for i, row in df.iterrows():
            dict = {
                "name": row["Exercise "],
                "equipment": row["Primary Equipment "],
                "region": row["Body Region"],
                "primary_group": row["Target Muscle Group "],
                "secondary_group": row["Secondary Muscle"],
                "tertiary_group": row["Tertiary Muscle"],
                "force": row["Force Type"],
                "mechanics": row["Mechanics"],
                "laterality": row["Laterality"],
                "difficulty": row["Difficulty Level"]
            }

            exist = supabase.from_("exercises")\
            .select("id")\
            .eq(column="name", value=row["Exercise "])\
            .execute().data

            if len(exist) != 0:
                continue

            supabase.from_("exercises")\
            .insert(dict)\
            .execute()
        
        return JSONResponse(status_code=201, content={"message":True})
    
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to POST exercise, error: {str(e)}")


# ---------- PUT ----------
@router.put("/sets/{id}", tags=['Fitness'])
def update_set(id: int, set_in: Sets):
    try:
        _set = supabase.from_("sets")\
        .select("id")\
        .eq(column="id", value=id)\
        .execute().data

        if len(_set) != 0:
            supabase.from_("sets")\
            .update({
                "reps": set_in.reps,
                "weight": set_in.weight
            })\
            .eq(column="id", value=id)\
            .execute()

            return JSONResponse(status_code=200, content={'message':True})

        else:
            return HTTPException(status_code=404, detail=f"Unable to Find set with id: {id}")

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to UPDATE set, error: {str(e)}")

# ---------- DELETE ----------
@router.put("/sets/{id}", tags=['Fitness'])
def delete_set(id: int):
    try:
        _set = supabase.from_("sets")\
        .select("id")\
        .eq(column="id", value=id)\
        .execute().data

        if len(_set) != 0:
            # Delete the set
            supabase.from_("sets")\
            .delete()\
            .eq(column="id", value=id)\
            .execute()

            # Delete the workout with that sid
            supabase.from_("workouts")\
            .delete()\
            .eq(column="sid", value=id)\
            .execute()

            return JSONResponse(status_code=200, content={'message':True})

        else:
            return HTTPException(status_code=404, detail=f"Unable to Find set with id: {id}")

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to DELETE set, error: {str(e)}")