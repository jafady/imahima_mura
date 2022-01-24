from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
# from django.db import close_old_connections
from channels.db import database_sync_to_async
import urllib.parse

@database_sync_to_async
def get_user(token):
    try:
        token = Token.objects.get(key=token)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner
    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    """
    Token authorization middleware for Django Channels 3
    """

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        # headers = dict(self.scope['headers'])
        decoded_qs = urllib.parse.parse_qs(self.scope["query_string"])
        if b'token' in decoded_qs:
            receive_token = decoded_qs.get(b'token').pop().decode()
            self.scope['user'] = await get_user(receive_token)
        else:
            self.scope['user'] = AnonymousUser()
        return await self.inner(self.scope, receive, send)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))