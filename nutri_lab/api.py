from typing import Any
from django.http import HttpRequest
from ninja import NinjaAPI
from plataforma.api import plataforma_router 
from ninja.security import HttpBasicAuth
from django.contrib import auth
from ninja.errors import ValidationError, HttpError

class BasicAuth(HttpBasicAuth):
    def authenticate(self, request: HttpRequest, username: str, password: str):
        user = auth.authenticate(username=username, password=password)
        if user:
            return user.id


api = NinjaAPI()

api.add_router('plataforma', plataforma_router)

@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    print(exc.errors)  # <--------------------- !!!!
    return api.create_response(request, {"detail": exc.errors}, status=422)

