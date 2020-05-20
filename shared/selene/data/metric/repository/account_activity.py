# Mycroft Server - Backend
# Copyright (C) 2020 Mycroft AI Inc
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
"""CRUD operations for the account_activity table in the metrics schema."""
from datetime import date

from ..entity.account_activity import AccountActivity
from ...repository_base import RepositoryBase


class AccountActivityRepository(RepositoryBase):
    """Query and maintain the account_activity table."""

    def __init__(self, db):
        super(AccountActivityRepository, self).__init__(db, __file__)

    def increment_accounts_added(self):
        """Increment the accounts added metric on the account activity table."""
        request = self._build_db_request(sql_file_name="increment_accounts_added.sql")
        row_updated = self.cursor.update(request)
        if not row_updated:
            self._add_account_activity_row(added=1)

    def increment_accounts_deleted(self):
        """Increment the deleted accounts metric on the account activity table."""
        request = self._build_db_request(sql_file_name="increment_accounts_deleted.sql")
        row_updated = self.cursor.update(request)
        if not row_updated:
            self._add_account_activity_row(deleted=1)

    def _add_account_activity_row(self, **kwargs):
        """Adds a row to the account activity table for a day that does not exist."""
        activity = dict(
            added=kwargs.get("added", 0),
            deleted=kwargs.get("deleted", 0),
            active=kwargs.get("active", 0),
            active_open_dataset=kwargs.get("active_open_dataset", 0),
            active_member=kwargs.get("active_member", 0),
        )
        request = self._build_db_request(
            sql_file_name="add_account_activity.sql", args=activity
        )
        self.cursor.insert(request)

    def get_activity_by_date(self, activity_date: date) -> AccountActivity:
        """Returns the account activity metrics for the given date."""
        return self._select_one_into_dataclass(
            dataclass=AccountActivity,
            sql_file_name="get_account_activity_by_date.sql",
            args=dict(activity_date=activity_date),
        )
