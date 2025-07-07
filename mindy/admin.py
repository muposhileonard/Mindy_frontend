@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'flagged', 'auto_hidden')
    search_fields = ('transcript',)


def __str__(self):
    return f"{self.created_by.username} - {self.post_type} - {self.created_at.date()}"
