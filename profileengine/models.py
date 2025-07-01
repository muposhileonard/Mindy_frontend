from django.contrib.auth import get_user_model
from django.db import models
from authengine.models import MindyUser

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(MindyUser, on_delete=models.CASCADE, related_name='profile')

    username = models.CharField(max_length=30, unique=True)
    surname = models.CharField(max_length=50)
    birthday = models.DateField()
    gender = models.CharField(max_length=10)
    education = models.CharField(max_length=100, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profiles_pics/',null=True, blank=True)
    display_badges = models.JSONField(default=list, blank=True)
    is_private = models.BooleanField(default=False)
    hide_birthday = models.BooleanField(default=False)
    hide_last_active = models.BooleanField(default=False)
    allowed_viewers = models.ManyToManyField(User, blank=True, related_name='can_view_profiles')
    # Analytics
    last_active = models.DateTimeField(auto_now=True)
    content_count = models.IntegerField(default=0)
    username_history = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"@{self.username}"



    def __str__(self):
        return f"{self.user.contact} Profile"

