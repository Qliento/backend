from rest_framework import serializers
from .models import *

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class PartnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partnership
        fields = ("header", "description", )

class PartnershipInfoSerializer(serializers.ModelSerializer):
    partnership = PartnershipSerializer(many=True)
    class Meta:
        model = PartnershipInfo
        fields = ("partnership", )


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"
        
class HaveQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HaveQuestion
        fields = "__all__"
        read_only_fields = ("id", )