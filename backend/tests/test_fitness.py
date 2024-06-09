import httpx

url = 'http://localhost:4000'

# ---------- WORKOUTS ----------
def test_get_workouts():
    response = httpx.get(f'{url}/fitness/workouts', params={"uid": 1, "date": "2001/01/01"})
    assert response.status_code == 200
    assert response.json()[0] == {
        "id": 2,
        "uid": 1,
        "eid": 1,
        "sid": 2,
        "date": "2001/01/01"
    }

def test_get_workout():
    response = httpx.get(f'{url}/fitness/workouts/1')
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "uid": 1,
        "eid": 1,
        "sid": 1,
        "date": "2024/06/08"
    }


def test_add_workout_set

# ---------- SETS ----------
def test_get_set():
    response = httpx.get(f'{url}/fitness/sets/1')
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "reps": 10,
        "weight": 110
    }

# ---------- EXERCISES ----------
def test_get_exercise():
    response = httpx.get(f'{url}/fitness/exercises/1')
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Stability Ball Dead Bug",
        "equipment": "Stability Ball",
        "region": "Midsection",
        "primary_group": "Abdominals",
        "secondary_group": "None",
        "tertiary_group": "None",
        "force": "Other",
        "mechanics": "Compound",
        "laterality": "Contralateral",
        "difficulty": "Beginner"
    }