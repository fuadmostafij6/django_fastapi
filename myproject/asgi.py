import os
import django
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

# Set the default settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Initialize Django (especially important if you access the ORM or Django settings)
django.setup()

# Import FastAPI routers after Django is setup
from accounts.api import router as accounts_router

# Initialize FastAPI app
fastapi_app = FastAPI()
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include FastAPI router with a prefix (/api)
fastapi_app.include_router(accounts_router, prefix="/api")

# Mount Django's ASGI app (using a WSGI middleware for Django)
from starlette.middleware.wsgi import WSGIMiddleware
from django.core.wsgi import get_wsgi_application

django_app = get_wsgi_application()
fastapi_app.mount("", WSGIMiddleware(django_app))
fastapi_app.mount("/static", StaticFiles(directory="staticfiles"), name="static")

# Expose as the ASGI callable
application = fastapi_app
