from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from fastapi import APIRouter, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserCreate, UserResponse, LoginRequest

from .database import get_db
from django.contrib.auth.hashers import make_password, check_password
from sqlalchemy.future import select
router = APIRouter()
User = get_user_model()


@router.post("/register/", response_model=UserResponse)
async def register(user: UserCreate,):
    user_exists = await sync_to_async(
        lambda: User.objects.filter(username=user.username).exists()
    )()
    if user_exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    email_exists = await sync_to_async(
        lambda: User.objects.filter(email=user.email).exists()
    )()
    if email_exists:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Create the new user and add it to the session
    # await sync_to_async(CustomUser.objects.create_user)(
    #     username=user_data.username,
    #     email=user_data.email,
    #     password=user_data.password,
    #     age=user_data.age,
    #     phone_number=user_data.phone_number
    # )

    new_user = await sync_to_async(User.objects.create_user)(
        username=user.username,
        email=user.email,
        password=user.password,
        bio=user.bio,
        profile_picture=user.profile_picture
    )
    profile_picture_url = str(new_user.profile_picture) if new_user.profile_picture else None
    return  {
    "id": new_user.id,
    "username": new_user.username,
    "email": new_user.email,
    "bio": new_user.bio,
    "profile_picture": profile_picture_url,
}
from django.core.handlers.asgi import ASGIRequest
from django.contrib.auth import authenticate, login
from io import BytesIO




@router.post("/login/", response_model=UserResponse)
async def login_user(login_data: LoginRequest, request: Request):
    # Create proper ASGIRequest with session support
    body_file = BytesIO(await request.body())
    django_request = ASGIRequest(
        scope=request.scope,
        body_file=body_file,
    )
    from django.contrib.sessions.middleware import SessionMiddleware
    from django.contrib.auth.middleware import AuthenticationMiddleware
    # Add session middleware
    session_middleware = SessionMiddleware(lambda req: None)
    await sync_to_async(session_middleware.process_request)(django_request)

    # Add auth middleware
    auth_middleware = AuthenticationMiddleware(lambda req: None)
    await sync_to_async(auth_middleware.process_request)(django_request)

    # Authenticate user
    user = await sync_to_async(authenticate)(
        request=django_request,
        username=login_data.username,
        password=login_data.password
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Perform login
    await sync_to_async(login)(django_request, user)

    # Save session
    await sync_to_async(django_request.session.save)()

    # Get profile picture URL
    profile_picture = str(user.profile_picture) if user.profile_picture else None

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "bio": user.bio,
        "profile_picture": profile_picture
    }