import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from database import supabase
from models.fitness import Sets, Workouts, Exercises
from datetime import datetime

router = APIRouter(
    prefix="/fitness",
    responses={404: {"message": "Not Found"}}
)

# ---------- SUPPORTED EXERCISES ----------
@router.get("/support_exercises/names", tags=['Support Exercises'])
def get_exercises_names():
    try:
        exercises = supabase.from_("support_exercises")\
        .select("id, name")\
        .execute().data

        return JSONResponse(status_code=200, content=exercises)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET support_exercises, error: {str(e)}")

@router.get("/support_exercises/{id}", tags=['Support Exercises'])
def get_exercise(id: int):
    try:
        exercise = supabase.from_("support_exercises")\
        .select("*")\
        .eq(column="id", value=id)\
        .execute().data[0]

        return JSONResponse(status_code=200, content=exercise)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET support_exercises, error: {str(e)}")
    
@router.post("/support_exercises/generate", tags=['Support Exercises'])
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

            exist = supabase.from_("support_exercises")\
            .select("id")\
            .eq(column="name", value=row["Exercise "])\
            .execute().data

            if len(exist) != 0:
                continue

            supabase.from_("support_exercises")\
            .insert(dict)\
            .execute()
        
        return JSONResponse(status_code=201, content={"message":True})
    
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to POST exercise, error: {str(e)}")

# ---------- EXERCISES ----------
@router.get("/exercises", tags=['Exercises'])
def get_exercises(wid: int):
    try:

        exercises = supabase.from_("exercises")\
        .select("*")\
        .eq(column="wid", value=wid)\
        .execute().data
        
        return JSONResponse(status_code=200, content=exercises)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET exercises, error: {str(e)}")

@router.get("/exercises/{id}", tags=['Exercises'])
def get_exercise(id: int):
    try:

        exercises = supabase.from_("exercises")\
        .select("*")\
        .eq(column="id", value=id)\
        .execute().data
        
        return JSONResponse(status_code=200, content=exercises)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET exercises, error: {str(e)}")
    
@router.post("/exercises", tags=['Exercises'])
def add_exercises(exercise: Exercises):
    try:
        # Insert Set and return the sid
        supabase.from_("sets")\
        .insert({
            "reps": exercise.reps,
            "weight": exercise.weight
        })\
        .execute()

        exercise.sid = supabase.from_("sets")\
        .select("id")\
        .order(column="id", desc=True)\
        .limit(size=1)\
        .execute().data[0]["id"]

        
    except Exception as e:
        return HTTPException(status_code=422, detail=f"Unable to POST set, error: {str(e)}")    

    try:
        # Insert Exercise
        supabase.from_("exercises")\
        .insert({
            "wid": exercise.wid,
            "eid": exercise.eid,
            "sid": exercise.sid
        })\
        .execute()

        return JSONResponse(status_code=201, content={
            "wid": exercise.wid,
            "eid": exercise.eid,
            "sid": exercise.sid
        })

    except Exception as e:
        return HTTPException(status_code=422, detail=f"Unable to POST exercise, error: {str(e)}")    

# ---------- SETS ----------
@router.get("/sets/{id}", tags=['Sets'])
def get_set(id: int):
    try:
        _set = supabase.from_("sets")\
        .select("*")\
        .eq(column="id", value=id)\
        .execute().data[0]

        return JSONResponse(status_code=200, content=_set)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET set, error: {str(e)}")
    
@router.put("/sets/{id}", tags=['Sets'])
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
    
@router.put("/sets/{id}", tags=['Sets'])
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
    
# ---------- WORKOUTS ----------
@router.get("/workouts", tags=['Workouts'])
def get_workouts(uid: int, date: str, name: str):

    # Validate Date
    try:
        datetime.fromisoformat(date)
    except ValueError:
        return HTTPException(status_code=404, detail=f"Date does not meet format Date does not meet format YYYY-mm-ddT00:00:00: {date}")

    # Validate User exist
    try:
        user = supabase.from_("users")\
        .select("*")\
        .eq(column="id", value=uid)\
        .limit(size=1)\
        .execute().data

        if len(user) == 0:
            return HTTPException(status_code=404, detail=f"Unable to Find User with id: {uid}")

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET user, error: {str(e)}")

    # Get workouts
    try:
        workouts = supabase.from_("workouts")\
        .select("*")\
        .eq(column="uid", value=uid)\
        .eq(column="date", value=date)\
        .eq(column="name", value=name)\
        .execute().data
        
        return JSONResponse(status_code=200, content=workouts)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET workouts, error: {str(e)}")
    

@router.get("/workouts/{id}", tags=['Workouts'])
def get_workout(id: int):
    try:
        workout = supabase.from_("workouts")\
        .select("*")\
        .eq(column="id", value=id)\
        .execute().data[0]

        return JSONResponse(status_code=200, content=workout)

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET workout, error: {str(e)}")
    
@router.post("/workouts", tags=['Workouts'])
def add_workout(workout: Workouts):
    try:
        supabase.from_("workouts")\
        .insert({
            "uid": workout.uid,
            "name": workout.name,
            "date": workout.date,
            "duration": workout.duration
        })\
        .execute()

        return JSONResponse(status_code=201, content={
            "uid": workout.uid,
            "name": workout.name,
            "date": workout.date,
            "duration": workout.duration
        })

    except Exception as e:
        return HTTPException(status_code=422, detail=f"Unable to POST workout, error: {str(e)}")
    
@router.put("/workouts/{id}", tags=['Workouts'])
def update_workout(id: int, workout: Workouts):
    try:
        workout_exist = supabase.from_("workouts")\
        .select("id")\
        .eq(column="id", value=id)\
        .execute().data

        if len(workout_exist) != 0:
            supabase.from_("workouts")\
            .update({
                "uid": workout.uid,
                "name": workout.name,
                "date": workout.date,
                "duration": workout.duration
            })\
            .eq(column="id", value=id)\
            .execute()

            return JSONResponse(status_code=200, content={'message':True})

        else:
            return HTTPException(status_code=404, detail=f"Unable to Find workout with id: {id}")

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to UPDATE workout, error: {str(e)}")
    
@router.delete("/workouts/{id}", tags=['Workouts'])
def delete_workout(id: int):

    # Validate Workout exists
    try:
        _workout = supabase.from_("workouts")\
        .select("id")\
        .eq(column="id", value=id)\
        .limit(size=1)\
        .execute().data

        if len(_workout) == 0:
            return HTTPException(status_code=404, detail=f"Unable to Find workout with id: {id}")

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET workout, error: {str(e)}")
    
    # Get Exercises
    try:
        exercises = supabase.from_("exercises")\
        .select("*")\
        .eq(column="wid", value=_workout[0]['id'])\
        .execute().data

        sids = [int(_['sid']) for _ in exercises]
        eids = [int(_['id']) for _ in exercises]
        
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to GET exercises, error: {str(e)}")
    
    # Delete Sets
    try:
        # Delete the set
        supabase.from_("sets")\
        .delete()\
        .in_(column="id", values=sids)\
        .execute()
    
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to DELETE set, error: {str(e)}")

    # Delete Exercises
    try:
        # Delete the set
        supabase.from_("exercises")\
        .delete()\
        .in_(column="id", values=eids)\
        .execute()
    
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to DELETE exercise, error: {str(e)}")

    # Delete Workout
    try:
        supabase.from_("workouts")\
        .delete()\
        .eq(column="id", value=id)\
        .execute()

        return JSONResponse(status_code=200, content={'message':True})

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unable to DELETE workout, error: {str(e)}")