from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import MindyUser
from .serializers import RegisterSerializer, LoginSerializer
# pip install twilio
from twilio.rest import Client
from django.conf import settings

def send_verification_code(contact):
    code = PhoneOTP.generate_code()

    PhoneOTP.objects.update_or_create(
        contact=contact,
        defaults={'code': code, 'verified': False}
    )

    client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)
    message = client.messages.create(
        body=f"Your Mindy verification code is: {code}",
        from_=settings.TWILIO_PHONE,
        to=contact
    )

    return code


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.validated_data['contact']
            password = serializer.validated_data['password']
            user = authenticate(contact=contact, password=password)
            if user:
                return Response({'message': 'Login successful!'}, status=200)
            return Response({'error': 'Invalid credentials'}, status=401)
        return Response(serializer.errors, status=400)

# Create your views here.






