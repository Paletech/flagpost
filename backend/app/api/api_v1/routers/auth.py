import os
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core import security
from app.core.auth import authenticate_user, get_current_user, sign_up_new_user
from app.core.s3.session import AWSSession
from app.db.session import get_db

auth_router = r = APIRouter()


@r.get("/aws_token")
async def get_sts_credentials(current_user=Depends(get_current_user)):
    role_arn = os.getenv("AWS_ROLE_ARN")
    session = AWSSession()
    async with session.client("sts") as sts:
        assumed_role = await sts.assume_role(RoleArn=role_arn, RoleSessionName="image-session", DurationSeconds=120)
    credentials: dict = assumed_role["Credentials"]
    return {
        "accessKeyId": credentials.get("AccessKeyId"),
        "secretAccessKey": credentials.get("SecretAccessKey"),
        "sessionToken": credentials.get("SessionToken")
    }


@r.post("/token")
async def login(
    db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    if user.is_superuser:
        permissions = "admin"
    else:
        permissions = "user"
    access_token = security.create_access_token(
        data={"sub": user.email, "permissions": permissions, "userId": str(user.id)},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@r.post("/signup")
async def signup(
    db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = sign_up_new_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    if user.is_superuser:
        permissions = "admin"
    else:
        permissions = "user"
    access_token = security.create_access_token(
        data={"sub": user.email, "permissions": permissions},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
