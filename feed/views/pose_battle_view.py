# feed/views/pose_battle_view.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from feed.models import PoseBattleEntry
from feed.serializers.pose_battle_serializer import PoseBattleSerializer

class PoseBattleViewSet(viewsets.ModelViewSet):
    queryset = PoseBattleEntry.objects.all()
    serializer_class = PoseBattleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(challenger=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        battle = self.get_object()
        if battle.opponent != request.user:
            return Response({'error': 'Not authorized'}, status=403)
        if battle.accepted:
            return Response({'detail': 'Already accepted'})
        battle.accepted = True
        battle.started_at = timezone.now()
        battle.save()
        return Response({'detail': 'Battle accepted'})

    @action(detail=True, methods=['post'])
    def deny(self, request, pk=None):
        battle = self.get_object()
        if battle.opponent != request.user:
            return Response({'error': 'Not authorized'}, status=403)
        battle.denied = True
        battle.save()
        return Response({'detail': 'Battle denied'})

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        battle = self.get_object()
        user = request.user
        if user in battle.voted_users.all():
            return Response({'detail': 'Already voted'}, status=400)

        choice = request.data.get("choice")
        if choice == "challenger":
            battle.challenger_votes += 1
        elif choice == "opponent":
            battle.opponent_votes += 1
        else:
            return Response({'error': 'Invalid choice'}, status=400)

        battle.voted_users.add(user)
        battle.save()
        return Response({'detail': 'Vote counted'})


        
