from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Gmail Schedule Watcher",
    description="Schedule Gmail messages and cancel them on thread updates",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Gmail Schedule Watcher API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

