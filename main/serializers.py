from rest_framework import serializers
from .models import *




class MobAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobApp
        fields = ('description', "image", "url") 

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ( 'info', )

class ContactInfoSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)
    class Meta:
        model = ContactInfo
        fields = ("contacts", )

class MainPageSerializer(serializers.ModelSerializer):
    mob_app = MobAppSerializer()
    сontacts = ContactInfoSerializer()

    class Meta:
        model = MainPage
        fields = ("mob_app", "сontacts", )
        



