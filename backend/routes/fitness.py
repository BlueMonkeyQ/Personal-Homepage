import pandas as pd
from typing import Any
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from database import supabase
from datetime import datetime
from models.fitness import Exercise, Sets, Workouts

router = APIRouter(
    prefix="/fitness",
    tags=["fitness"],
    responses={404: {"message": "Not Found"}}
)

# ---------- GET ----------
@router.get("/workout")
def get_workouts(uid: int, date: datetime):
    try:
        workouts = supabase.from_("workouts")\
        .select("*")\
        .eq(column="uid", value=uid)\
        .eq(column="date", value=date)\
        .execute().data

        return JSONResponse(status_code=201, content=workouts)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET workouts, error: {str(e)}")
    
# ---------- POST ----------
@router.post("/workout")
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
        .execute().data[0]

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
    
@router.post("/exercise/generate")
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


# ---------- DELETE ----------