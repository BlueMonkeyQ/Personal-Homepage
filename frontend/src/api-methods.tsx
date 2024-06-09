export async function getWorkouts(uid: string, date: string) {
    const res = await fetch(`http://localhost:4000/fitness/workouts?uid=${uid}&date=${date}`)

    if (!res.ok) {
        throw new Error('Failed to fetch data')
    }

    return res.json()
}

export async function addWorkout(formData: { reps: string, weight: string, date: string }) {
    const { reps, weight, date } = formData;

    const res = await fetch('http://localhost:4000/fitness/workouts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        next: { revalidate: 3600 },
        body: JSON.stringify({
            "uid": 0,
            "eid": 0,
            "sid": 0,
            "reps": parseInt(reps),
            "weight": parseInt(weight),
            "date": date
        }),
    });

    if (!res.ok) {
        throw new Error('Failed to fetch data');
    }

    return res.json();
}
