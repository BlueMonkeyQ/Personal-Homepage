from pydantic import BaseModel
from datetime import datetime

class Exercise(BaseModel):
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

class Sets(BaseModel):
    reps: int
    weight: float

class Workouts(BaseModel):
    uid: int
    eid: int
    sid: int = None
    reps: int = None
    weight: float = None
    date: str