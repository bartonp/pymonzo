from datetime import datetime
from typing import List

class MonzoObject:
    _required_keys = ... # type: list

    def _parse_special_fields(self, data: List[str]) -> None: ...


class MonzoAccount(MonzoObject):
    id = ... # type: unicode
    description = ... # type: unicode
    created = ... # type: datetime
    closed = ... # type: bool
    type = ... # type: unicode
    account_number = ... # type: unicode
    sort_code = ... # type: unicode

    def transactions(self, update: bool) -> List[MonzoTransaction]: ...



class MonzoBalance(MonzoObject):
    balance = ... # type: int
    currency = ... # type: unicode
    spend_today = ... # type: int


class MonzoToken(MonzoObject):
    user_id = ... # type: unicode
    access_token = ... # type: unicode
    expires_in = ... # type: int
    token_type = ... # type: unicode
    client_id = ... # type: int


class MonzoPot(MonzoObject):
    id = ... # type: unicode
    name = ... # type: unicode
    created = ... # type: datetime
    style = ... # type: unicode
    balance = ... # type: int
    currency = ... # type: unicode
    updated = ... # type: datetime
    deleted = ... # type: bool

    def deposit(self, account_id: unicode, amount: int) -> MonzoPot: ...
    def withdraw(self, account_id: unicode, amount: int) -> MonzoPot: ...



class MonzoMerchant(MonzoObject):
    address = ... # type: dict
    created = ... # type: datetime
    group_id = ... # type: unicode
    id = ... # type: unicode
    logo = ... # type: unicode
    emoji = ... # type: unicode
    name = ... # type: unicode
    category = ... # type: unicode


class MonzoTransaction(MonzoObject):
    account_balance = ... # type: int
    amount = ... # type: int
    created = ... # type: datetime
    currency = ... # type: unicode
    description = ... # type: unicode
    id = ... # type: unicode
    merchant = ... # type: MonzoMerchant
    metadata = ... # type: unicode
    notes = ... # type: unicode
    is_load = ... # type: bool
    declined = ... # type: bool
    decline_reason = ... # type: unicode
    settled = ... # type: datetime