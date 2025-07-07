# feed/serializers/report_serializer.py

from rest_framework import serializers
from feed.models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'post', 'comment', 'reason', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']
