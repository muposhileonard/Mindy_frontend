from collections import Counter

REACTION_ICONS = {
    'Love': '😍',
    'Haha': '😂',
    'Wow': '😮',
    'Sad': '😢',
    'Like': '👍',
    'Yay': '🎉',
    'Aww': '🥺',
    'Whatever': '🙄'
}

def get_emoji_reaction_summary(reaction_queryset):
    """
    Takes a queryset or list of reaction types (strings) and returns a dict
    mapping emoji to count.
    Example: {'😂': 4, '😍': 2}
    """
    if hasattr(reaction_queryset, 'values_list'):
        reactions = reaction_queryset.values_list('type', flat=True)
    else:
        reactions = reaction_queryset
    count = Counter(reactions)
    return {REACTION_ICONS.get(k, k): v for k, v in count.items()}
