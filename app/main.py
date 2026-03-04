from fastapi import FastAPI
from app.api.v1 import user, auth, profile, file_upload

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(file_upload.router, prefix="/files", tags=["File Upload"])