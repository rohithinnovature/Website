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
from .models import UserProfile


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
# @csrf_exempt
def signup2(request):
    username = request.data.get('username')
    email = request.data.get('email')
    
    if not username or not email:
        return JsonResponse({'error': 'Both username and email must be provided'}, status=400)
    
    try:
        user = User.objects.get(username=username)
        user_profile, created = UserProfile.objects.get_or_create(username=user)
        user_profile.email = email
        user_profile.save()
        
        return JsonResponse({'message': 'UserProfile updated successfully'})
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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
def get_user_profile(request):
    username = request.data.get('usernam')
    if not username:
        return JsonResponse ({'error': 'Username not provided'}, status=400)
    
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(username=user)
        
        response_data = {
            'username': user_profile.username.username,
            'first_name':user_profile.first_name,
            'last_name': user_profile.last_name,
            'email': user_profile.email,
            'phone_number': user_profile.phone_number,
            'date_of_birth': user_profile.date_of_birth,
        }
        
        return JsonResponse(response_data)
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'UserProfile does not exist'}, status=404)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def save_profile(request):
    userpro = request.data.get('usernam')
    if not userpro:
        return JsonResponse ({'error': 'Username not provided'}, status=400)
    err = {}

    try :
        k = userpro.get('first_name')
        if ord(k[0]) < 65 or ord(k[0]) > 90 : 
            err.update({'errorf':'First name must start with capital letter'})
            print("capital error in fname")
        k = userpro.get('last_name')
        if ord(k[0]) < 65 or ord(k[0]) > 90 : 
            err['errorl'] = 'Last name must start with capital letter'
            print("capital error in fname")
        if userpro.get('phone_number') :
            k = userpro.get('phone_number')
            print('ivide')    
            if len(k) != 10 : 
                print('phone number error')
                err['errorP'] = "Phone number must be 10 digits"
        if err : return JsonResponse(err)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    try:
        user = User.objects.get(username=userpro.get('username'))
        user_profile, created = UserProfile.objects.get_or_create(username=user)
        user_profile.first_name = userpro.get('first_name')
        user_profile.last_name = userpro.get('last_name')
        user_profile.date_of_birth = userpro.get('date_of_birth')
        user_profile.phone_number = userpro.get('phone_number')
        user_profile.save()
        return JsonResponse({'message': 'UserProfile updated successfully'})
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'UserProfile does not exist'}, status=404)