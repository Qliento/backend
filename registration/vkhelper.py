from social_core.backends import vk
from social_core.backends.base import BaseAuth


class VK:

    @staticmethod
    def validate(auth_token):

        try:
            lol = vk.VKontakteOpenAPI(BaseAuth)
            user = lol.user_data(access_token=auth_token)
            print('lol', user)
            return user

        except:
            return {"detail": "The token is invalid or expired."}
