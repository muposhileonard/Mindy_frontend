from celery import shared_task
from django.core.serializers import serialize
from django.contrib.auth import get_user_model
from profileengine.models import Profile

@shared_task
def export_user_data(user_id):
    try:
        user = get_user_model().objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        
        # Serialize data
        user_json = serialize('json', [user])
        profile_json = serialize('json', [profile])
        
        # Save to file (you can also zip later)
        with open(f'/data/data/com.termux/files/home/mindy/exports/user_{user_id}_data.json', 'w') as f:
            f.write(user_json + "\n" + profile_json)

        return f"User {user.username}'s data exported successfully."
    
    except Exception as e:
        return f"Failed to export user data: {str(e)}"

 # your logic here
    pass
