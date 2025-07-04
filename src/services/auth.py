from typing import Optional
from datetime import datetime, timedelta

from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as rep_users
from src.configuration.config import SECRET_KEY, ALGORITHM


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    async def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[float] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now() + timedelta(minutes=15)
        to_encode.update({
            "iat": datetime.now(),
            "exp": expire,
            "scope": "access_token"
        })
        # print(f"{ALGORITHM} - {SECRET_KEY}")
        encoded_access_token = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        return encoded_access_token

    async def create_refresh_token(
        self,
        data: dict,
        expires_delta: Optional[float] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now() + timedelta(days=7)
        to_encode.update({
            "iat": datetime.now(),
            "exp": expire,
            "scope": "access_token"
        })
        # print(f"{ALGORITHM} - {SECRET_KEY}")
        encoded_refresh_token = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        # print(f"{ALGORITHM} - {SECRET_KEY}")
        try:
            payload = jwt.decode(
                refresh_token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
            if payload:
                email = payload['sub']
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token"
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

    async def get_current_user(
        self,
        token: str = Depends(oauth2_schema),
        db: Session = Depends(get_db)
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"www-Authenticate": "Bearer"},
        )

        try:
            # print(f"{ALGORITHM} - {SECRET_KEY}")
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
            if payload['scope'] == 'access_token':
                email = payload['sub']
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await rep_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user


auth_service = Auth()

current_active_user = auth_service.get_current_user
