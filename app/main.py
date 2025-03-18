from fastapi import FastAPI

app = FastAPI(
    title="To-Do List API",
    description="A REST API for managing to-do lists with user authentication",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to the To-Do List API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)