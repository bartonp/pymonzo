# -*- coding: utf-8 -*-
"""
Monzo API objects related code
"""
from __future__ import unicode_literals

import six
from dateutil.parser import parse as parse_date

from pymonzo.utils import CommonMixin


class MonzoObject(CommonMixin):
    """
    Base class for all Monzo API objects
    """
    _required_keys = []

    def __init__(self, data, client=None):
        """
        Takes Monzo API response data and maps the keys as class properties.
        It requires certain keys to be present to make sure we got the response
        we wanted.

        :param data: response from Monzo API request
        :type data: dict
        """
        missing_keys = [
            k for k in self._required_keys
            if k not in data
        ]
        if missing_keys:
            raise ValueError(
                "Passed data doesn't have all required keys "
                "(missing keys: {})".format(','.join(missing_keys))
            )

        self._client = client

        self._raw_data = data.copy()
        data_copy = data.copy()

        # Take care of parsing non-standard fields
        self._parse_special_fields(data_copy)

        # Map the rest of the fields automatically
        self.__dict__.update(**data_copy)

    def _parse_special_fields(self, data):
        """
        Helper method that parses special fields to Python objects
        """
        pass


class MonzoAccount(MonzoObject):
    """
    Class representation of Monzo account
    """
    _required_keys = ['id', 'description', 'created']

    def __init__(self, *args, **kwargs):
        super(MonzoAccount, self).__init__(*args, **kwargs)
        self.__cached_transactions = None

    def _parse_special_fields(self, data):
        """
        Helper method that parses special fields to Python objects

        :param data: response from Monzo API request
        :type data: dict
        """
        self.created = parse_date(data.pop('created'))

    def transactions(self, update=False):
        if update or self.__cached_transactions is None:
            self.__cached_transactions = self._client.transactions(account_id=self.id,
                                                                   reverse=True,
                                                                   expand_merchant=True)

        return self.__cached_transactions

    def balance(self):
        return self._client.balance(account_id=self.id)


class MonzoBalance(MonzoObject):
    """
    Class representation of Monzo account balance
    """
    _required_keys = ['balance', 'currency', 'spend_today']


class MonzoTransaction(MonzoObject):
    """
    Class representation of Monzo transaction
    """
    _required_keys = [
        'account_balance', 'amount', 'created', 'currency', 'description',
        'id', 'merchant', 'metadata', 'notes', 'is_load',
    ]

    def _parse_special_fields(self, data):
        """
        Helper method that parses special fields to Python objects

        :param data: response from Monzo API request
        :type data: dict
        """
        self.created = parse_date(data.pop('created'))

        if data.get('settled'):  # Not always returned
            self.settled = parse_date(data.pop('settled'))

        # Merchant field can contain either merchant ID or the whole object
        if data.get('merchant') and not isinstance(data['merchant'], six.text_type):
            self.merchant = MonzoMerchant(data=data.pop('merchant'))

        if data.get('decline_reason'):  # Just to be able to easily get an item as declined
            self.declined = True
        else:
            self.declined = False

        self.transaction_type = data.get('scheme')



class MonzoMerchant(MonzoObject):
    """
    Class representation of Monzo merchants
    """
    _required_keys = [
        'address', 'created', 'group_id', 'id',
        'logo', 'emoji', 'name', 'category',
    ]

    def _parse_special_fields(self, data):
        """
        Helper method that parses special fields to Python objects

        :param data: response from Monzo API request
        :type data: dict
        """
        self.created = parse_date(data.pop('created'))


class MonzoToken(MonzoObject):
    """
    Class representation of Monzo Tokens
    """
    _required_keys = ['user_id', 'access_token', 'expires_in', 'token_type', 'client_id']


class MonzoPot(MonzoObject):
    """
    Class representation of Monzo account
    """
    _required_keys = ['id', 'name', 'created', 'style', 'balance', 'currency', 'updated', 'deleted']

    def _parse_special_fields(self, data):
        """
        Helper method that parses special fields to Python objects

        :param data: response from Monzo API request
        :type data: dict
        """
        self.created = parse_date(data.pop('created'))
        self.updated = parse_date(data.pop('updated'))


    def deposit(self, account_id, amount):
        pot = self._client.pot_deposit(account_id=account_id, pot_id=self.id, amount=amount)
        self.__update(pot)

    def withdraw(self, account_id, amount):
        pot = self._client.pot_withdraw(account_id=account_id, pot_id=self.id, amount=amount)
        self.__update(pot)

    def __update(self, pot):
        self.created = pot.created
        self.updated = pot.updated
        data = pot._raw_data.copy()
        data.pop('created')
        data.pop('updated')
        self.__dict__.update(**data)

