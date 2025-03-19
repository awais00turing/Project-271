from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi

from app.api.endpoints import auth, tasks
from app.core.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="To-Do List API",
    description="""
    A REST API for managing to-do lists with user authentication.
    
    ## Features
    
    * **User Authentication**: Register and login with JWT tokens
    * **Task Management**: Create, read, update, and delete tasks
    * **Security**: Password hashing and token-based authentication
    
    ## Authentication
    
    To use the API, first register a user, then login to get a JWT token.
    Use this token in the Authorization header for all protected endpoints.
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@todoapi.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    auth.router, 
    prefix="/api/auth", 
    tags=["authentication"],
    responses={401: {"description": "Authentication failed"}},
)
app.include_router(
    tasks.router, 
    prefix="/api/tasks", 
    tags=["tasks"],
    responses={
        401: {"description": "Authentication failed"},
        403: {"description": "Forbidden - Not enough permissions"},
        404: {"description": "Task not found"},
    },
)

@app.get("/")
async def root():
    return {"message": "Welcome to the To-Do List API. Visit /docs for API documentation."}

# Custom OpenAPI schema to include JWT authentication
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add JWT security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter JWT token obtained from the login endpoint",
        }
    }
    
    # Apply security to all operations except login and register
    for path_key, path in openapi_schema["paths"].items():
        for method, operation in path.items():
            # Skip login and register endpoints
            if path_key == "/api/auth/login" or path_key == "/api/auth/register":
                continue
            
            # Add security requirement to all other endpoints
            operation["security"] = [{"Bearer Auth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
