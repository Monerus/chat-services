from app.config import settings
import jwt

from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/user/verify-code/")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            settings.PUBLIC_KEY_PATH.read_text(),
            algorithms=[settings.JWT_ALGORITHM]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}",
        ) 

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="В токене отсутствует user_id",
        )

    return user_id