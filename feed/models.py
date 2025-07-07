from django.db import models
from django.conf import settings
import re
from authengine.models import MindyUser
from mutagen.mp3 import MP3
import os
from django.core.exceptions import ValidationError
#from feed.utils.transcript import generate_transcript
from django.utils import timezone
from datetime import timedelta

User = MindyUser

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    usage_count = models.PositiveIntegerField(default=0)
    trending_score = models.FloatField(default=0.0)

    def __str__(self):
        return f"#{self.name}"


class Post(models.Model):
    POST_TYPES = [
        ("text", "Text"),
        ("glimpse", "Glimpse"),
        ("pose_battle", "Pose Battle"),
        ("article", "Article"),
        ("poll","poll")
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    content = models.TextField(blank=True)
    transcript = models.TextField(blank=True, null=True)
    media = models.FileField(upload_to="posts/media/", blank=True, null=True)
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default="text")
    saves_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)    
    mentions = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="mentioned_in", blank=True)
    allow_reactions = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    reactions_count = models.PositiveIntegerField(default=0)
    reaction_summary = models.JSONField(default=dict, blank=True)
    views_count = models.PositiveIntegerField(default=0)

    age_rating = models.CharField(max_length=10, default="15+")
    lang = models.CharField(max_length=10, default="en")
    pulse_score = models.FloatField(default=0.0)
    # In Post class
    text_color = models.CharField(max_length=20, default="black")
    bg_color = models.CharField(max_length=20, default="brown")  # paper brown
    font_style = models.CharField(max_length=30, default="serif")  # Or let frontend choose

 
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    transcript = models.TextField(null=True, blank=True)
    flagged = models.BooleanField(default=False)
    auto_hidden = models.BooleanField(default=False)
    
    
    def save(self, *args, **kwargs):
        if self.video:
            #self.transcript = generate_transcript(self.video.path)
            self.check_for_banned_words()
        super().save(*args, **kwargs)

    def check_for_banned_words(self):
        banned_words = ["kill", "rape", "bomb", "shoot", "suicide", "hate", "nude", "terror", "slaughter"]
        text = (self.transcript or "").lower()
        if any(bad in text for bad in banned_words):
            self.flagged = True
            self.auto_hidden = True

    def __str__(self):
        return f"{self.author} - {self.post_type} - {self.created_at.date()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_mentions()

    def update_mentions(self):
        usernames = self.extract_usernames()
        users = User.objects.filter(profile__username__in=usernames)
        self.mentions.set(users)

    def extract_usernames(self):
        return re.findall(r'@(\w+)', self.content or "")

        
        
        def save(self, *args, **kwargs):
            if self.video and not self.transcript:
                try:
                    #self.transcript = generate_transcript(self.video.path)
                    pass
                except Exception as e:
                    print(f"Transcript error: {e}")
            super().save(*args, **kwargs)


            BAD_WORDS = ['badword1', 'badword2', 'offensiveword']
            
            def contains_bad_words(text):
                return any(bad_word in text.lower() for bad_word in BAD_WORDS)

                if contains_bad_words(self.transcript):
                    self.is_flagged = True



class PostReaction(models.Model):
    REACTIONS = [
        ("like", "Like"),
        ("love", "Love"),
        ("haha", "Haha"),
        ("wow", "Wow"),
        ("sad", "Sad"),
        ("yay", "Yay"),
        ("aww", "Aww"),
        ("whatever", "Whatever"),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=REACTIONS)
    reacted_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('post', 'user')  # Only one reaction per user per post

    def __str__(self):
        return f"{self.user} reacted {self.type} to Post {self.post.id}"


class CommentReply(models.Model):
    class CommentReply(models.Model):
        comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies')
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        text = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
    
        def __str__(self):
            return f"Reply by {self.user} on Comment {self.comment.id}"
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author} to Comment {self.comment.id}"






  # install mutagen


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    voice_note = models.FileField(upload_to='comments/audio/', null=True, blank=True)
    audio_reply = models.FileField(upload_to='comment_replies/audio/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.voice_note:
            ext = os.path.splitext(self.voice_note.name)[1]
            if ext.lower() != '.mp3':
                raise ValidationError("Only MP3 files are allowed.")
            audio = MP3(self.voice_note)
            if audio.info.length > 40:
                raise ValidationError("Audio comments must be under 40 seconds.")

    def save(self, *args, **kwargs):
        self.full_clean()  # run validation
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.user} on {self.post.id}"


class CommentReaction(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)  # e.g., love, haha, sad, wow...

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')  # Prevent double reaction

    def __str__(self):
        return f"{self.user} reacted to Comment {self.comment.id} with {self.type}"


class Repost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reposts')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# feed/models.py

class Report(models.Model):
    REPORT_CHOICES = [
        ('spam', 'Spam'),
        ('abuse', 'Abuse'),
        ('nudity', 'Nudity'),
        ('hate', 'Hate Speech'),
        ('violence', 'Violence'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True)
    reason = models.CharField(max_length=50, choices=REPORT_CHOICES)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PostSave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_bookmark = models.BooleanField(default=False)
    saved_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.is_bookmark and timezone.now() > self.saved_at + timedelta(days=7)



class PostBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(days=7)


# feed/models.py

class ArticlePost(models.Model):
    post = models.OneToOneField('Post', on_delete=models.CASCADE, related_name='article')
    text = models.TextField()
    font = models.CharField(max_length=50, default='Roboto')
    font_size = models.IntegerField(default=16)
    text_color = models.CharField(max_length=10, default='#000')
    background_color = models.CharField(max_length=10, default='#f4e6d5')

    
# feed/models.py
# feed/models.py

class PoseBattleEntry(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="pose_battle")
    challenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pose_challenges")
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pose_challenges_received")

    challenger_media = models.FileField(upload_to="pose_battles/challenger/")
    opponent_media = models.FileField(upload_to="pose_battles/opponent/", null=True, blank=True)

    description = models.CharField(max_length=250)
    accepted = models.BooleanField(default=False)
    denied = models.BooleanField(default=False)
    voted_users = models.ManyToManyField(User, related_name="pose_battle_votes", blank=True)
    challenger_votes = models.IntegerField(default=0)
    opponent_votes = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def is_live(self):
        return self.accepted and not self.ended_at

    def winner(self):
        if not self.ended_at:
            return None
        if self.challenger_votes > self.opponent_votes:
            return self.challenger
        elif self.opponent_votes > self.challenger_votes:
            return self.opponent
        return "tie"


class PollOption(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='poll_options')
    option_text = models.CharField(max_length=100)
    votes = models.PositiveIntegerField(default=0)
        
    def __str__(self):
        return f"{self.option_text} - {self.votes} votes"


class PostAnalytics(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='analytics')
    views = models.PositiveIntegerField(default=0)
    saves = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    reach_score = models.FloatField(default=0.0)




