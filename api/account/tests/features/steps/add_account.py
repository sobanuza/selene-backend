# Mycroft Server - Backend
# Copyright (C) 2019 Mycroft AI Inc
# SPDX-License-Identifier: 	AGPL-3.0-or-later
#
# This file is part of the Mycroft Server.
#
# The Mycroft Server is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""Step functions for the new account feature of the single sign on API."""
from binascii import b2a_base64
from datetime import date, datetime

from behave import given, then, when
from flask import json
from hamcrest import assert_that, equal_to, is_in, not_none

from selene.data.account import AccountRepository, PRIVACY_POLICY, TERMS_OF_USE
from selene.data.metric import AccountActivityRepository

new_account_request = dict(
    termsOfUse=True,
    privacyPolicy=True,
    login=dict(
        federatedPlatform=None,
        federatedToken=None,
        email=b2a_base64(b"bar@mycroft.ai").decode(),
        password=b2a_base64(b"bar").decode(),
    ),
)


@given("a user completes new account setup")
def build_new_account_request(context):
    """Add the new account information to the context."""
    context.new_account_request = new_account_request


@given("user does not specify an email address")
def remove_email_from_request(context):
    """Remove the email address from the context for federated account testing."""
    del context.new_account_request["login"]["email"]


@when("the new account request is submitted")
def call_add_account_endpoint(context):
    """Call the single sign on API endpoint to add the account"""
    context.client.content_type = "application/json"
    context.response = context.client.post(
        "/api/account",
        data=json.dumps(context.new_account_request),
        content_type="application/json",
    )


@then("the account will be added to the system")
def check_db_for_account(context):
    """Ensure the account was correctly added to the database."""
    acct_repository = AccountRepository(context.db)
    account = acct_repository.get_account_by_email("bar@mycroft.ai")
    # add account to context so it will deleted by cleanup step
    context.accounts["bar"] = account
    assert_that(account, not_none())
    assert_that(account.email_address, equal_to("bar@mycroft.ai"))

    assert_that(len(account.agreements), equal_to(2))
    for agreement in account.agreements:
        assert_that(agreement.type, is_in((PRIVACY_POLICY, TERMS_OF_USE)))
        assert_that(agreement.accept_date, equal_to(str(date.today())))


@then("the new account will be reflected in the account activity metrics")
def check_db_for_account_metrics(context):
    """Ensure the new account is accurately reflected in the metrics."""
    acct_activity_repository = AccountActivityRepository(context.db)
    account_activity = acct_activity_repository.get_activity_by_date(
        datetime.utcnow().date()
    )
    if context.account_activity is None:
        assert_that(account_activity.added, equal_to(1))
    else:
        assert_that(
            account_activity.added, equal_to(context.account_activity.added + 1)
        )
