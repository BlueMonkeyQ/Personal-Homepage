// Get
export async function getWorkouts(uid: string, date: string) {
    const res = await fetch(`http://localhost:4000/fitness/workouts?uid=${uid}&date=${date}`, {
        mode: "cors"
    })

    if (!res.ok) {
        console.log(res.ok)
        throw new Error('Failed to fetch data')
    }

    return res.json()
}
// Post
export async function addWorkout(formData: { workoutName: string, date: string, duration: string }) {
    const { workoutName, date, duration } = formData;

    const res = await fetch('http://localhost:4000/fitness/workouts', {
        method: 'POST',
        mode: "cors",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            uid: 2,
            name: workoutName,
            date: date,
            duration: parseInt(duration, 10)
        }),
    });

    if (!res.ok) {
        const errorDetail = await res.json();
        throw new Error(`Failed to fetch data: ${errorDetail.message}`);
    }

    return res.json();
}

// Delete
export async function deleteWorkout(wid: string) {
    const res = await fetch(`http://localhost:4000/fitness/workouts/${wid}`, {
        method: 'DELETE',
        mode: 'cors',
        headers: {
            'Accept': 'application/json',
        }
    });

    if (!res.ok) {
        const errorDetail = await res.json();
        throw new Error(`Failed to fetch data: ${errorDetail.message}`);
    }

    return res.json();
}

// Patch