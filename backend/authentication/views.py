from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.models import SocialAccount, SocialToken
from dj_rest_auth.registration.views import SocialLoginView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import post
import requests
from allauth.socialaccount.helpers import complete_social_login

from core.settings import EMAIL_CONFIRM_REDIRECT_BASE_URL, PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL


def email_confirm_redirect(request, key):
    return HttpResponseRedirect(f"{EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/")


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )


def google_login(request):
    token = request.data.get('token')
    if not token:
        return JsonResponse({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Verify token with Google's OAuth2 API
    response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
    if response.status_code != 200:
        return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    user_info = response.json()

    # Extract useful fields
    email = user_info.get('email')
    if not email:
        return JsonResponse({'error': 'Email not provided in token'}, status=status.HTTP_400_BAD_REQUEST)

    email_verified = user_info.get('email_verified')
    if not email_verified:
        return JsonResponse({'error': 'Email not verified by Google'}, status=status.HTTP_400_BAD_REQUEST)

    # Ensure token is intended for our app (by checking audience field)
    aud = user_info.get('aud')
    if aud != 'YOUR_GOOGLE_CLIENT_ID':  # Replace with your actual Google Client ID
        return JsonResponse({'error': 'Token is not valid for this app'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the token is expired
    exp = int(user_info.get('exp'))
    if exp < int(time.time()):
        return JsonResponse({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)

    # Use part of the email before '@' as username
    username = email.split('@')[0]

    # Check if user already exists or create a new user
    user, created = User.objects.get_or_create(
        email=email,
        defaults={'username': username, 'is_active': True}
    )

    # If using Django Allauth, create a social account or log the user in
    social_account = SocialAccount.objects.filter(user=user, provider='google').first()
    if not social_account:
        # If the social account doesn't exist, create one
        social_account = SocialAccount(user=user, provider='google', uid=user_info['sub'])
        social_account.save()

    # Handle the login process via allauth
    social_login = complete_social_login(request._request, social_account)

    if isinstance(social_login, JsonResponse):
        # Return any errors if allauth provides them
        return social_login

    return JsonResponse({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)

class OAuthCallbackView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)

        #code = request.data.get('code')
        #if not code:
        #    return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the token using Google's tokeninfo endpoint
        response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
        if response.status_code != 200:
            return Response({'error': 'Failed to fetch tokens from Google'}, status=status.HTTP_400_BAD_REQUEST)

        token_info = response.json()

        # Extract user information from token
        email = token_info.get('email')
        if email:
            first_name = token_info.get('given_name', '')
            last_name = token_info.get('family_name', '')

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],  # You can generate a more complex username if needed
                    'first_name': first_name,
                    'last_name': last_name,
                    # Add other fields as necessary
                }
            )

            try:
                # Generate and return token
                from rest_framework.authtoken.models import Token
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'key': token.key}, status=status.HTTP_200_OK)
            except ValueError as e:
                # Invalid token
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Email not found in token"}, status=status.HTTP_400_BAD_REQUEST)

## To BE REMOVED
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/api/auth/callback/google"
    client_class = OAuth2Client
## To BE REMOVED