from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user, role, auth  # Import auth router
from app.utils.database import engine, Base

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="MyPro Backend",
    description="Backend for MyPro application with user registration, login, and role management.",
    version="1.0.0"
)

# Add CORS middleware (optional, for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (update this for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(user.router, prefix="/api/users", tags=["users"])
app.include_router(role.router, prefix="/api/roles", tags=["roles"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])  # Include auth router

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to MyPro Backend!"}