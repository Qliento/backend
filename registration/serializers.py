from rest_framework import serializers
from .models import QAdmins, Users, Clients, UsersConsentQliento
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import password_validation
from research.models import Research
from research.serializers import CountrySerializer, HashtagSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image
from rest_framework_recaptcha.fields import ReCaptchaField


class AdditionalInfoToken(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        try:
            QAdmins.objects.get(admin_status_id=self.user.id)
            data['user'] = 'partner'
        except ObjectDoesNotExist:
            pass

        try:
            Clients.objects.get(client_status_id=self.user.id)
            data['user'] = 'client'
        except ObjectDoesNotExist:
            pass

        return data


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
        respondents_data.set_password(validated_data['password'])
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
    photo = serializers.ImageField(required=False)

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
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance


class UsersInfoSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(max_length=160, write_only=True)
    photo = serializers.ImageField(read_only=True)

    class Meta:
        model = Users
        fields = [
                  "id",
                  "name",
                  "surname",
                  "photo",
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
        fields = '__all__'
        model = QAdmins

    def create(self, validated_data):
        initial_data = validated_data.pop('admin_status')
        user = Users.objects.create_user(**initial_data)
        researcher = QAdmins.objects.create(admin_status=user, **validated_data)
        return researcher

    def to_representation(self, instance):
        response = super(QAdminSerializer, self).to_representation(instance)
        del response.get('admin_status')['password']
        return response


class RawDataUser(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)

    class Meta:
        fields = ["photo",
                  "name",
                  "surname",
                  "email",
                  "phone_number"]
        model = Users


class QAdminUpdateSerializer(serializers.ModelSerializer):
    admin_status = RawDataUser(required=True, many=False)

    class Meta:
        fields = '__all__'
        model = QAdmins

    def update(self, instance, validated_data):
        user_retrieved = instance.admin_status
        take_from_data = validated_data.pop('admin_status')
        for i in take_from_data:
            print(i)
            user_retrieved.name = take_from_data.get('name', user_retrieved.name)
            user_retrieved.surname = take_from_data.get('surname', user_retrieved.surname)
            user_retrieved.phone_number = take_from_data.get('phone_number', user_retrieved.phone_number)
            user_retrieved.photo = take_from_data.get('photo', user_retrieved.photo)
            user_retrieved.save()

        instance.about_me = validated_data.get('about_me', instance.about_me)
        instance.position = validated_data.get('position', instance.position)
        instance.save()
        return instance


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

    def to_representation(self, instance):
        response = super(ClientSerializer, self).to_representation(instance)
        del response.get('client_status')['password']
        return response


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


class CleanedResearchSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(many=True, read_only=True)
    country = CountrySerializer(many=True, read_only=True)
    about_author = serializers.ReadOnlyField(source='author.about_me')

    class Meta:
        model = Research
        fields = ['image', 'author_id', 'name', 'date', 'pages',
                  'hashtag', 'country', 'new_price', 'old_price', 'id', 'status', 'about_author']


class CleanedFileOnly(serializers.ModelSerializer):

    class Meta:
        model = Research
        fields = ['research']


class CleanedDemoOnly(serializers.ModelSerializer):

    class Meta:
        model = Research
        fields = ['demo']


class UserConsentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsersConsentQliento
        fields = '__all__'
