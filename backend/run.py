from fastapi import FastAPI
from starlette.responses import RedirectResponse
from routes import users
from routes import fitness

app = FastAPI(debug=True)
app.include_router(users.router)
app.include_router(fitness.router)


@app.get("/")
async def home():
    return RedirectResponse(url="/docs/")