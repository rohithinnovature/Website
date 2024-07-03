# authentication/views.py

import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login as django_login , logout
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .serializers import UserSerializer
from django_recaptcha.fields import ReCaptchaField  # Assuming this is from django-recaptcha
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User



@api_view(['POST'])
@permission_classes([AllowAny])
# @csrf_exempt
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)        

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        captcha_token = request.data.get('token')

        if not verify_recaptcha(captcha_token):
           return Response({'error': 'CAPTCHA verification failed.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)
            return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def verify_recaptcha(token):
    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': token
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    return response.json().get('success', False)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def get_user_email(request):
    usernam = request.data.get('usernam')
    if not usernam:
        return JsonResponse ({'error': 'Username not provided'}, status=400)
    # Retrieve the user object by username
    user = get_object_or_404(User, username=usernam)
    
    # Get the email from the user object
    email = user.email
    
    # Return the email as a JSON response
    return JsonResponse({'email': email})




# @api_view(['POST'])
# def user_logout(request):
#     if request.user.is_authenticated:
#         logout(request)
#         return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
#     return Response({'error': 'Not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def empty_path(request):
#     # """
#     # Placeholder view for an empty path.
#     # """
#     return Response({'message': 'This is an empty path.'})
