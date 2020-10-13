from rest_framework import serializers
from .models import QAdmins, Users, Clients
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import password_validation
from PIL import Image
from rest_framework_recaptcha.fields import ReCaptchaField


class UsersSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(max_length=160, write_only=True)
    # recaptcha = ReCaptchaField()

    class Meta:
        model = Users
        fields = ["name",
                  "surname",
                  "password",
                  "password_check",
                  "email",
                  "phone_number",
                  ]
        extra_kwargs = {'password_check': {'required': True}}

    def validate(self, data):
        if data['password'] != data['password_check'] or len(data['password']) < 8:

            raise serializers.ValidationError("Пароли должны совпадать и содержать более 8 символов")
        else:
            data.pop('password_check')

        return data

    def create(self, validated_data):

        respondents_data = Users.objects.create_user(**validated_data)
        respondents_data.save()
        return respondents_data

    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance


class UsersUpdateSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()

    class Meta:
        model = Users
        fields = ["photo",
                  "name",
                  "surname",
                  "email",
                  "phone_number",
                  ]

    def create(self, validated_data):

        respondents_data = Users.objects.create_user(**validated_data)
        respondents_data.save()
        return respondents_data

    def update(self, instance, validated_data):
        instance.photo = validated_data.get('photo', instance.photo)
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance


class UsersInfoSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(max_length=160, write_only=True)

    class Meta:
        model = Users
        fields = [
                  "name",
                  "surname",
                  "password",
                  "password_check",
                  "email",
                  "phone_number",
                  ]
        extra_kwargs = {'password_check': {'required': True}}

    def validate(self, data):
        if data['password'] != data['password_check'] or len(data['password']) < 8:

            raise serializers.ValidationError("Пароли должны совпадать и содержать более 8 символов")
        else:
            data.pop('password_check')

        return data


class QAdminSerializer(serializers.ModelSerializer):
    admin_status = UsersInfoSerializer(required=True, many=False)

    class Meta:
        fields = ["logo", "admin_status"]
        model = QAdmins

    def create(self, validated_data):
        initial_data = validated_data.pop('admin_status')
        user = Users.objects.create_user(**initial_data)
        researcher = QAdmins.objects.create(admin_status=user, **validated_data)
        return researcher


class ClientSerializer(serializers.ModelSerializer):
    client_status = UsersInfoSerializer(required=True, many=False)

    class Meta:
        fields = ["client_status"]
        model = Clients

    def create(self, validated_data):
        initial_data = validated_data.pop('client_status')
        user = Users.objects.create_user(**initial_data)
        qlient = Clients.objects.create(client_status=user, **validated_data)
        return qlient


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Users
        fields = ['token']


class UpdatePassword(serializers.Serializer):
    old_password = serializers.CharField(max_length=160, required=True)
    new_password = serializers.CharField(max_length=160, required=True)
    password_check = serializers.CharField(max_length=160, write_only=True, required=True)

    def validate_old_password(self, data):
        user = self.context['request'].user
        if not user.check_password(data):
            raise serializers.ValidationError(
                _('Your old password was entered incorrectly. Please enter it again.')
            )
        return data

    def validate(self, data):
        if data['new_password'] != data['password_check']:
            raise serializers.ValidationError({'password_check': _("The two password fields didn't match.")})
        password_validation.validate_password(data['new_password'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user
