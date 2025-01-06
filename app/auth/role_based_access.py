

# auth/role_based_access.py
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from auth.authentication import decode_auth_token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def role_required(role: str):
    def role_check(token: str = Depends(oauth2_scheme)):
        decoded_data = decode_auth_token(token)
        if isinstance(decoded_data, str):  # If an error message was returned
            raise HTTPException(status_code=403, detail=decoded_data)
        
        user_role = decoded_data.get("role")
        if user_role != role:
            raise HTTPException(status_code=403, detail="Access denied: Admins only")
        return decoded_data  # You can also return the user info if needed
    return role_check