from rest_framework import authentication


class BearerAuthentication(authentication.TokenAuthentication):
    keyword = 'Bearer'

    def authenticate_header(self, request):
        return self.keyword
