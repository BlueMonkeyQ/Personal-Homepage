import httpx

url = 'http://localhost:4000'

# ---------- WORKOUTS ----------
def test_get_workouts():

    # Passing
    response = httpx.get(f'{url}/fitness/workouts', params={"uid": 1, "date": "2001-01-01T00:00:00"})
    assert response.status_code == 200
    assert response.json()[0] == {
        "id": 2,
        "uid": 1,
        "eid": 1,
        "sid": 2,
        "date": "2001-01-01T00:00:00"
    }

    # Failing Bad uid
    response = httpx.get(f'{url}/fitness/workouts', params={"uid": 0, "date": "2001-01-01T00:00:00"})
    assert response.json()['status_code'] == 404
    assert response.json()['detail'] == "Unable to Find User with id: 0"

    # Failing Missing uid
    response = httpx.get(f'{url}/fitness/workouts', params={"date": "2001-01-01T00:00:00"})
    assert response.status_code == 422
    
    # Failing Bad date
    response = httpx.get(f'{url}/fitness/workouts', params={"uid": 0, "date": "2001-01-01T00:00:00"})
    assert response.json()['status_code'] == 404
    assert response.json()['detail'] == "Unable to Find User with id: 0"

    # Failing Missing date
    response = httpx.get(f'{url}/fitness/workouts', params={"uid": 1,  "date": "2001-01-01T00:00:00"})
    assert response.json()['status_code'] == 404
    assert response.json()['detail'] == "Date does not meet format Date does not meet format YYYY-mm-ddT00:00:00: 2001-01-01"

def test_get_workout():

    # Passing
    response = httpx.get(f'{url}/fitness/workouts/1')
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "uid": 1,
        "eid": 1,
        "sid": 1,
        "date": "2001-01-01T00:00:00"
    }

    # Failing Bad id
    response = httpx.get(f'{url}/fitness/workouts/0')
    assert response.json()['status_code'] == 500

def test_add_workout_set():

    # Passing
    json = {
        "uid": 1,
        "eid": 1,
        "sid": 0,
        "reps": 10,
        "weight": 100,
        "date": "2001-01-01T00:00:00"
    }
    response = httpx.post(f'{url}/fitness/workouts', json=json)
    assert response.status_code == 201

    expected_keys = {"uid", "eid", "sid", "date"}
    assert expected_keys.issubset(response.json().keys())

    # Failing Missing data
    json = {
        "uid": 1,
        "eid": 1,
        "sid": 0,
        "reps": 10,
        "weight": 100
    }
    response = httpx.post(f'{url}/fitness/workouts', json=json)
    assert response.status_code == 422

# ---------- SETS ----------
def test_get_set():

    # Passing
    response = httpx.get(f'{url}/fitness/sets/1')
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "reps": 10,
        "weight": 110
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
    response = httpx.put(f'{url}/fitness/sets/1', json=json)
    assert response.status_code == 200
    assert response.json() == {'message':True}

    # Reset Value
    json = {
        "reps": 10,
        "weight": 110
    }
    response = httpx.put(f'{url}/fitness/sets/1', json=json)
    assert response.status_code == 200
    assert response.json() == {'message':True}

    #

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