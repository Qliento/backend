from rest_framework import serializers
from .models import *

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class PartnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partnership
        fields = "__all__"

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"
