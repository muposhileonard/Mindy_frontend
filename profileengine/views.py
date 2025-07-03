from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, permissions
from .models import Profile
from rest_framework.views import  APIView
from .serializers import ProfileSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

class ProfileUpdateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request):
        ...

class ProfileCreateView(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        # Enforce privacy
        if profile.is_private and request.user not in profile.allowed_viewers.all() and request.user != profile.user:     
             return Response({"detail": "This profile is private"}, status=403)


        serializer = ProfileSerializer(profile)
        data = serializer.data


        if profile.hide_birthday:
            data.pop('birthday', None)


        if profile.hide_last_active:
            data.pop('last_active', None)

        
        return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found."}, status=404)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_my_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=404)

    serializer = ProfileSerializer(profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile)
    data = serializer.data

    if profile.hide_birthday:
        data.pop('birthday', None)

    if profile.hide_last_active:
        data.pop('last_active', None)

    return Response(data)





@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_my_profile(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)








@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_my_profile(request):
    profile = Profile.objects.get(user=request.user)
    new_username = request.data.get("username")

    # ✅ Track username change
    if new_username and new_username != profile.username:
        if profile.username not in profile.username_history:
            profile.username_history.append(profile.username)

    serializer = ProfileSerializer(profile, data=request.data, partial=True)

    if serializer.is_valid():
        instance = serializer.save()
        # ✅ Save history change AFTER serializer does its thing
        instance.username_history = profile.username_history
        instance.save()
        return Response(ProfileSerializer(instance).data)
    else:
        return Response(serializer.errors, status=400)








# profileengine/views.py

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=404)

    # Privacy logic
    if profile.is_private and profile.user != request.user and request.user not in profile.allowed_viewers.all():
        return Response({'detail': 'This profile is private'}, status=403)

    data = ProfileSerializer(profile).data

    # Remove sensitive fields if not owner
    if profile.user != request.user:
        if profile.hide_birthday:
            data.pop('birthday', None)
        if profile.hide_last_active:
            data.pop('last_active', None)

    return Response(data)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_my_data(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=404)

    data = ProfileSerializer(profile).data
    response = Response(data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="mindy_user_data.json"'
    return response
