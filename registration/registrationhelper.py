from django.contrib.auth import authenticate
from .models import Users, QAdmins, Clients
from qliento import settings
from rest_framework.exceptions import AuthenticationFailed


def register_social_user(provider, email, name, surname, who):
    filtered_user_by_email = Users.objects.filter(email=email)
    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].provider:

            registered_user = authenticate(email=email, password=settings.SOCIAL_SECRET)

            return {
                'email': registered_user.email,
                'user': registered_user.id,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using your social network')

    else:
        user = {
            'email': email,
            'password': settings.SOCIAL_SECRET,
            'name': name,
            'surname': surname
            }

        user = Users.objects.create_user(**user)
        user.is_active = True
        user.provider = provider
        user.save()

        if who == 'partner':
            QAdmins.objects.create(admin_status=user)
        else:
            Clients.objects.create(client_status=user)

        new_user = authenticate(username=email, password=settings.SOCIAL_SECRET)

        return {
            'email': new_user.email,
            'user': new_user.id,
            'tokens': new_user.tokens()
        }
