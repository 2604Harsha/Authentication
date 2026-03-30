# utils/role_checker.py
from fastapi import Depends, HTTPException, status
from utils.dependencies import get_current_user

def require_roles(*roles: str):
    def role_checker(user=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission"
            )
        return user
    return role_checker
