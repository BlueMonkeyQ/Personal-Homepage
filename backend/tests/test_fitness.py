import httpx

url = 'http://localhost:4000'

# ---------- WORKOUTS ----------
def test_get_workouts():

    # Passing
    params = {
        "uid": 1,
        "date": "2001-01-01T00:00:00"
    }
    response = httpx.get(f'{url}/fitness/workouts', params=params)
    assert response.status_code == 200
    expected_keys = {"id", "uid", "name", "date", "duration"}
    assert expected_keys.issubset(response.json()[0].keys())

    # Failing Bad id
    params = {
        "uid": 0,
        "date": "2001-01-01T00:00:00"
    }
    response = httpx.get(f'{url}/fitness/workouts', params=params)
    assert response.json()['status_code'] == 404
    assert response.json()['detail'] == "Unable to Find User with id: 0"

    # Failing Bad date
    params = {
        "uid": 1,
        "date": "2001"
    }
    response = httpx.get(f'{url}/fitness/workouts', params=params)
    assert response.json()['status_code'] == 404
    assert response.json()['detail'] == "Date does not meet format Date does not meet format YYYY-mm-ddT00:00:00: 2001"
    
def test_get_workout():

    # Passing
    response = httpx.get(f'{url}/fitness/workouts/18')
    assert response.status_code == 200
    assert response.json() == {
        "id": 18,
        "uid": 1,
        "name": "Test Workout",
        "date": "2001-01-01T00:00:00+00:00",
        "duration": 60,
    }

    # Failing Bad id
    response = httpx.get(f'{url}/fitness/workouts/0')
    assert response.json()['status_code'] == 500

def test_add_workout():

    # Passing Unique workout
    params = {
        "uid": 1,
        "date": "2001-01-01T00:00:00"
    }
    response = httpx.get(f'{url}/fitness/workouts', params=params)


    json = {
        "uid": 1,
        "name": f"Test Workout {len(response.json())}",
        "date": "2001-01-01T00:00:00",
        "duration": 60,
    }
    response = httpx.post(f'{url}/fitness/workouts', json=json)
    assert response.status_code == 201

    expected_keys = {"uid", "name", "date", "duration"}
    assert expected_keys.issubset(response.json().keys())

    # Failing Workout Exist
    json = {
        "uid": 1,
        "name": "Test Workout",
        "date": "2001-01-01T00:00:00",
        "duration": 60,
    }
    response = httpx.post(f'{url}/fitness/workouts', json=json)
    assert response.json()['status_code'] == 422

    # Failing Missing data
    json = {
        "uid": 1,
        "name": "Test Workout",
        "duration": 60,
    }
    response = httpx.post(f'{url}/fitness/workouts', json=json)
    assert response.status_code == 422

def test_update_workout():

    # Passing
    json = {
        "uid": 1,
        "name": "Testing Workout",
        "date": "2002-01-01T00:00:00",
        "duration": 45
    }
    response = httpx.put(f'{url}/fitness/workouts/18', json=json)
    assert response.status_code == 200
    assert response.json()['message'] == True

    response = httpx.get(f'{url}/fitness/workouts/18')
    assert response.status_code == 200
    assert response.json() == {
        "id": 18,
        "uid": 1,
        "name": "Testing Workout",
        "date": "2002-01-01T00:00:00+00:00",
        "duration": 45,
    }

    # Revert Back
    json = {
        "uid": 1,
        "name": "Test Workout",
        "date": "2001-01-01T00:00:00",
        "duration": 60
    }
    response = httpx.put(f'{url}/fitness/workouts/18', json=json)
    assert response.status_code == 200
    assert response.json()['message'] == True

    # Failing Missing Data
    json = {
        "uid": 1,
        "name": "Test Workout",
        "duration": 60
    }
    response = httpx.put(f'{url}/fitness/workouts/18', json=json)
    assert response.status_code == 422

    # Failing Invalid Date
    json = {
        "uid": 1,
        "name": "Test Workout",
        "date": "2001",
        "duration": 60
    }
    response = httpx.put(f'{url}/fitness/workouts/18', json=json)
    assert response.json()['status_code'] == 500

def test_delete_workout():

    # Passing

    # Create Workout
    json = {
        "uid": 1,
        "name": "Test Workout to be deleted",
        "date": "1900-01-01T00:00:00",
        "duration": 60,
    }
    response = httpx.post(f'{url}/fitness/workouts', json=json)
    assert response.status_code == 201

    # Create Exercise and Set
    json = {
        "wid": 2,
        "eid": 1,
        "sid": 0,
        "reps": 10,
        "weight": 100
    }
    response = httpx.post(f'{url}/fitness/exercise', json=json)
    assert response.status_code == 201

    # Delete Workout
    params = {
        "uid": 1,
        "date": "1900-01-01T00:00:00"
    }
    response = httpx.get(f'{url}/fitness/workouts', params=params)
    assert response.status_code == 200
    id = response.json()[0]['id']


    response = httpx.delete(f'{url}/fitness/workouts/{id}')
    assert response.status_code == 200
    assert response.json()['message'] == True

    # Failing Bad id
    response = httpx.delete(f'{url}/fitness/workouts/0')
    assert response.json()['status_code'] == 404
    assert response.json()['detail'] == "Unable to Find workout with id: 0"

# ---------- SETS ----------
def test_get_set():

    # Passing
    response = httpx.get(f'{url}/fitness/sets/9')
    assert response.status_code == 200
    assert response.json() == {
        "id": 9,
        "reps": 10,
        "weight": 100
    }

    # Failing Bad id
    response = httpx.get(f'{url}/fitness/sets/0')
    assert response.json()['status_code'] == 500

def test_update_set():

    # Passing
    json = {
        "reps": 20,
        "weight": 200
    }
    response = httpx.put(f'{url}/fitness/sets/9', json=json)
    assert response.status_code == 200
    assert response.json() == {'message':True}

    # Reset Value
    json = {
        "reps": 10,
        "weight": 110
    }
    response = httpx.put(f'{url}/fitness/sets/9', json=json)
    assert response.status_code == 200
    assert response.json() == {'message':True}

# ---------- SUPPORTED EXERCISES ----------
def test_get_exercises_via_names():

    # Passing
    response = httpx.get(f'{url}/fitness/support_exercises/name/squat')
    assert response.status_code == 200
    assert len(response.json()) == 10

    # Passing No Results
    response = httpx.get(f'{url}/fitness/support_exercises/name/doesnotexist')
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_get_exercise_via_id():
    response = httpx.get(f'{url}/fitness/support_exercises/1')
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

# ---------- EXERCISES ----------
def test_get_exercises():

    # Passing
    response = httpx.get(f'{url}/fitness/exercise/9')
    response.status_code == 200
    assert response.json() == {
        "id": 9,
        "wid": 2,
        "eid": 1,
        "sid": 9
    }

    # Failing Bad id
    response = httpx.get(f'{url}/fitness/exercise/0')
    assert response.json()['status_code'] == 500
    assert response.json()['detail'] == "Unable to GET exercise, error: list index out of range"


def test_add_exercises():
    # Passing
    json = {
        "wid": 2,
        "eid": 1,
        "sid": 0,
        "reps": 10,
        "weight": 100
    }
    response = httpx.post(f'{url}/fitness/exercise', json=json)
    assert response.status_code == 201
    expected_keys = {"wid", "eid", "sid"}
    assert expected_keys.issubset(response.json().keys())

    # Failing missing data
    json = {
        "sid": 0,
        "reps": 10,
        "weight": 100
    }
    response = httpx.post(f'{url}/fitness/exercise', json=json)
    assert response.status_code == 422

def test_update_exercise():
    
    # Passing
    json = {
        "wid": 100,
        "eid": 200,
        "sid": 0,
        "reps": 0,
        "weight": 0
    }
    response = httpx.put(f'{url}/fitness/exercise/9', json=json)
    assert response.status_code == 200
    assert response.json() == {'message':True}

    # Reset Value
    json = {
        "wid": 2,
        "eid": 1,
        "sid": 0,
        "reps": 0,
        "weight": 0
    }
    response = httpx.put(f'{url}/fitness/exercise/9', json=json)
    assert response.status_code == 200
    assert response.json() == {'message':True}


def test_delete_exercise():

    # Passing
    # Create Exercise
    json = {
        "wid": 2,
        "eid": 1,
        "sid": 0,
        "reps": 10,
        "weight": 100
    }
    response = httpx.post(f'{url}/fitness/exercise', json=json)
    assert response.status_code == 201
    id = response.json()['id']

    # Delete Exercise
    response = httpx.delete(f'{url}/fitness/exercise/{id}')
    assert response.status_code == 200
    assert response.json()['message'] == True

    # Failing Bad ID
    response = httpx.delete(f'{url}/fitness/exercise/0')
    assert response.json()['status_code'] == 404
    assert response.json()['detail'] == "Unable to Find exercise with id: 0"