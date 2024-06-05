from fastapi import FastAPI
from starlette.responses import RedirectResponse
from routes import users

app = FastAPI(debug=True)
app.include_router(users.router)

@app.get("/")
async def home():
    return RedirectResponse(url="/docs/")