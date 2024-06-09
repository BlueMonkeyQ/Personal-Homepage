import json
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from routes import users
from routes import fitness

tags_metadata = {}
with open("data/tags_metadata.json", 'r') as file:
    tags_metadata = json.load(file)


app = FastAPI(debug=True, openapi_tags=tags_metadata)
app.include_router(users.router)
app.include_router(fitness.router)


@app.get("/")
async def home():
    return RedirectResponse(url="/docs/")