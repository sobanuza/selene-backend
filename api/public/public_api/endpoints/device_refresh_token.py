import hashlib
import json
from http import HTTPStatus

from selene.api import PublicEndpoint, generate_device_login
from selene.util.auth import AuthenticationError


class DeviceRefreshTokenEndpoint(PublicEndpoint):

    ONE_DAY = 86400

    def __init__(self):
        super(DeviceRefreshTokenEndpoint, self).__init__()
        self.sha512 = hashlib.sha512()

    def get(self):
        headers = self.request.headers
        if 'Authorization' not in headers:
            raise AuthenticationError('Oauth token not found')
        token_header = self.request.headers['Authorization']
        if token_header.startswith('Bearer '):
            refresh = token_header[len('Bearer '):]
            session = self._refresh_session_token(refresh)
            if session:
                response = session, HTTPStatus.OK
            else:
                response = '', HTTPStatus.UNAUTHORIZED
        else:
            response = '', HTTPStatus.UNAUTHORIZED
        return response

    def _refresh_session_token(self, refresh: str):
        refresh_key = 'device.token.refresh:{}'.format(refresh)
        session = self.cache.get(refresh_key)
        if session:
            old_login = json.loads(session)
            device_id = old_login['uuid']
            self.cache.delete(refresh_key)
            return generate_device_login(device_id, self.cache)