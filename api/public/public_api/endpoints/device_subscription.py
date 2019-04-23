from http import HTTPStatus

from selene.api import PublicEndpoint
from selene.data.account import AccountRepository


class DeviceSubscriptionEndpoint(PublicEndpoint):
    def __init__(self):
        super(DeviceSubscriptionEndpoint, self).__init__()

    def get(self, device_id):
        self._authenticate(device_id)
        account = AccountRepository(self.db).get_account_by_device_id(device_id)
        if account:
            membership = account.membership
            response = (
                {'@type': membership.type if membership is not None else 'free'},
                HTTPStatus.OK
            )
        else:
            response = '', HTTPStatus.NO_CONTENT

        return response
