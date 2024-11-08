from fastapi import FastAPI
from routes.score_rfc import score
app = FastAPI()
app.include_router(score)

@app.get("/")
def read_root():
    return {"Hello": "World"}