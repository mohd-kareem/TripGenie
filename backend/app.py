from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from planner.routes import router as planner_router

app = FastAPI(title="TripGenie Travel Planner")

# Allow your frontend to access the API
origins = [
    "http://localhost",
    "http://localhost:5500",  # if you are using Live Server extension
    "*",  # allow all origins (for testing)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(planner_router, prefix="/planner", tags=["planner"])

@app.get("/")
async def root():
    return {"message": "TripGenie API is running 🚀"}