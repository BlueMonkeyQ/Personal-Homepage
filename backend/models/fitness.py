from pydantic import BaseModel

class Support_Exercises(BaseModel):
    name: str
    equipment: str
    region: str = None
    primary_group: str = None
    secondary_group: str = None
    tertiary_group: str = None
    force: str = None
    mechanics: str = None
    laterality: str = None
    difficulty: str = None

class Exercises(BaseModel):
    wid: int
    eid: int 
    sid: int 
    reps: int
    weight: float

class Sets(BaseModel):
    reps: int
    weight: float

class Workouts(BaseModel):
    uid: int
    name: str
    date: str
    duration: int