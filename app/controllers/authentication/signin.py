from typing import Optional, List

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from ninja import Router, Schema
from ninja.responses import Response
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken

from app.models import RefreshTokenStorage, User
from app.schema import ResponseSchema, LoginSchema, SignInResponsePayload

router = Router()

@router.post("signin", tags=["Authentication"])
def signin(request, payload: LoginSchema):
    try:
        user = authenticate(username=payload.email, password=payload.password)
        if user is None or not user.is_active:
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        token_obj, _ = RefreshTokenStorage.objects.get_or_create(user=user)
        token_obj.token = refresh_token
        token_obj.save()

        payload = SignInResponsePayload(
            user_id=str(user.id),
            user_email=user.email,
            access_token=access_token
        )

        payload = payload.dict()

        response_data = ResponseSchema(payload=payload, is_ok=True, message="User authenticated.", err_data=None)

        response = Response(response_data, status=201)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=60 * 60 * 24 * 7,
            secure=True,
            samesite="None"
        )
        return response
    except Exception as e:
        return Response(
            data={"error": {"name": "SIGNIN_ERROR", "details": f"An error occurred during signin, {e}"}},
            status=500
        )


@router.get("refresh", tags=["Authentication"])
def refresh_token(request):
    try:
        refresh_token = request.COOKIES.get('refresh_token', None)
        if not refresh_token:
            response = Response(status=403, data={'detail': "Invalid refresh token."})
            response.set_cookie('refresh_token', '', path='/')
            return response
        try:
            refresh_token_storage = RefreshTokenStorage.objects.get(token=refresh_token)
            user = refresh_token_storage.user
        except:
            response = Response(status=401, data={'detail': "Cannot find user."})
            response.set_cookie('refresh_token', '', path='/')
            return response
        try:
            refresh = RefreshToken.for_user(user)
        except:
            response = Response(status=401, data={'detail': "Refresh token has expired."})
            response.set_cookie('refresh_token', '', path='/')
            return response

        payload = {
            "access_token": str(refresh.access_token)
            }
        return Response(ResponseSchema(payload=payload, is_success=True, message="Token Refreshed.", err_data=None), status=200)
    except Exception as e:
        return Response(
            data={"error": {"name": "REFRESH_TOKEN_ERROR", "details": f"An error occurred getting refresh token, {e}"}},
            status=500
        )



@router.post('logout', auth=JWTAuth(), tags=["Authentication", ])
def logout(request):
    try:
        refresh_token = request.COOKIES.get('refresh_token', None)
        if refresh_token:
            token = RefreshTokenStorage.objects.filter(token=refresh_token)
            if token:
                token.delete()
        response = JsonResponse({"success": "Logged out"})
        response.delete_cookie('refresh_token')
        return response
    except Exception as e:
        return Response(
            data={"error": {"name": "LOGOUT_ERROR", "details": f"An error occurred logging out, {e}"}},
            status=500
        )