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
"""Setup the environment for the behavioral tests."""
from datetime import datetime

from behave import fixture, use_fixture

from account_api.api import acct
from selene.data.metric import AccountActivityRepository
from selene.testing.account import add_account, remove_account
from selene.testing.account_geography import add_account_geography
from selene.testing.agreement import add_agreements, remove_agreements
from selene.testing.text_to_speech import add_text_to_speech, remove_text_to_speech
from selene.testing.wake_word import add_wake_word, remove_wake_word
from selene.util.cache import SeleneCache
from selene.util.db import connect_to_db


@fixture
def acct_api_client(context):
    """Add a test fixture representing the account API."""
    acct.testing = True
    context.client_config = acct.config
    context.client = acct.test_client()

    yield context.client


def before_all(context):
    """Execute these steps before any tests run."""
    use_fixture(acct_api_client, context)
    context.db = connect_to_db(context.client_config["DB_CONNECTION_CONFIG"])
    agreements = add_agreements(context.db)
    context.terms_of_use = agreements[0]
    context.privacy_policy = agreements[1]
    context.open_dataset = agreements[2]


def after_all(context):
    """Execute these steps after all tests have run."""
    remove_agreements(
        context.db, [context.privacy_policy, context.terms_of_use, context.open_dataset]
    )


def before_scenario(context, _):
    """Setup steps to run before each scenario."""
    account = add_account(context.db)
    context.accounts = dict(foo=account)
    context.geography_id = add_account_geography(context.db, account)
    context.wake_word = add_wake_word(context.db)
    context.voice = add_text_to_speech(context.db)
    acct_activity_repository = AccountActivityRepository(context.db)
    context.account_activity = acct_activity_repository.get_activity_by_date(
        datetime.utcnow().date()
    )


def after_scenario(context, _):
    """Scenario-level cleanup.

    The database is setup with cascading deletes that take care of cleaning up[
    referential integrity for us.  All we have to do here is delete the account
    and all rows on all tables related to that account will also be deleted.
    """
    for account in context.accounts.values():
        remove_account(context.db, account)
    remove_wake_word(context.db, context.wake_word)
    remove_text_to_speech(context.db, context.voice)
    _clean_cache()


def _clean_cache():
    """Remove testing data from the Redis database."""
    cache = SeleneCache()
    cache.delete("pairing.token:this is a token")
