from rest_framework.routers import DefaultRouter
from feed.views.reaction_views import PostReactionViewSet
from feed.views.comment_reaction_view import CommentReactionViewSet
from django.urls import path, include
from feed.views.comment_view import CommentViewSet
from feed.views.comment_reply_views import CommentReplyViewSet
from feed.views.comment_view import CommentViewSet
from feed.views.save_view import PostSaveViewSet
from feed.views.repost_view import RepostViewSet
from feed.views.report_view import ReportViewSet
from feed.views.bookmark_view import PostBookmarkViewSet
from feed.views.post_view import PostViewSet
from feed.views.pose_battle_view import PoseBattleViewSet
from feed.views.analytics_view import PostAnalyticsView


router = DefaultRouter()
router.register(r'posts', PostViewSet, basename="post")
router.register(r'pose-battles',PoseBattleViewSet)
router.register(r'bookmarks',PostBookmarkViewSet)
router.register(r'saves', PostSaveViewSet)
router.register(r'reposts', RepostViewSet)
router.register(r'reports', ReportViewSet)
urlpatterns = router.urls
router.register(r'comments', CommentViewSet)
router.register(r'comment-replies', CommentReplyViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:pk>/analytics/',PostAnalyticsView.as_view(), name='post-analytics'),
]

router = DefaultRouter()
router.register(r"reactions", PostReactionViewSet, basename="reactions")
router.register(r'comment-reactions', CommentReactionViewSet, basename='comment-reaction')

urlpatterns += router.urls


