from fastapi import FastAPI

app = FastAPI(title="Mental Wellness Tracker API")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Mental Wellness Tracker API is running"}
