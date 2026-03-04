from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user, require_roles
from app.schemas.user import UserRead

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def read_profile(current_user=Depends(get_current_user)):
    return current_user


@router.get("/admin-data")
async def admin_endpoint(current_user=Depends(require_roles("admin"))):
    return {"msg": "Welcome Admin!"}
