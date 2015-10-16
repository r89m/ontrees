from datetime import datetime, timedelta
import json
import requests

"""
An unofficial module for interacting with the OnTrees finance management service.

Allows you to retrieve a list of your linked banks, linked accounts. You can also refresh your account balances
and retrieve a list of past transactions (limited to 90 days)
"""


class Client:

    _email = None
    _password = None
    _auth_token = None

    _app_id = "pxtBmMEKyC77Qvd2GCjepejf"            # The OnTrees web interface AppId
    _api_host = "https://prod-api.ontrees.com/"     # Prodution API host

    def __init__(self, email, password):

        self._email = email
        self._password = password

    def _make_request(self, method="GET", url=None, data=None, is_login_request=False, repeat_on_fail=True):

        # Authenticate if there is no auth token stored and this request isn't a login request
        if self._auth_token is None and is_login_request is not True:
            auth = self.login()
            if not auth:
                return False

        # Select the correct function
        if method == "GET":
            request_func = requests.get
        else:
            request_func = requests.post

        # Build the data body
        data_str = None
        if data is not None:
            data_str = json.dumps(data)

        # Build the end point url
        endpoint_url = "{0}{1}".format(self._api_host, url)

        # Send the request
        r = request_func(url=endpoint_url, data=data_str, headers=self._get_headers(is_login_request))

        # Check for invalid auth (expired token) - if so authenticate again and resend request
        if r.status_code == 401:    # 401 - Unathorized
            # If this was a login request or is the second attemp, stop here.
            if is_login_request or not repeat_on_fail:
                return False
            # Otherwise, try logging in and sending the request again
            else:
                # Login again
                self.login()
                # Resend the request, but set repeat_on_fail to false to prevent a loop
                return self._make_request(method, data, is_login_request, False)

        return r.json()

    def _get_headers(self, skip_auth_header=False):

        headers = {"AppId": self._app_id, "Content-Type": "application/json"}

        if not skip_auth_header:
            headers["Authorization"] = "Bearer {0}".format(self._auth_token)

        return headers

    # Public API
    def get_accounts(self, linked_banks=None):
        """
        Return a list of Accounts that are linked to your OnTrees account
        :param linked_banks: Previously retrieved list of accounts (saves making another web request)
        :return: a list of Accounts
        """

        # If no linked banks are supplied, retrieve them
        if linked_banks is None:
            linked_banks = self.get_linked_banks()

        if linked_banks:
            accounts = []
            for linked_bank in linked_banks:
                for account in linked_bank.get("Accounts"):
                    accounts.append(account)

            return accounts
        else:
            return False

    def get_linked_banks(self):
        """
        Return a list of banks that are linked to your OnTrees account.
        A list of accounts can also be retrieved from here.
        :return: a list of Linked Banks
        """
        links = self._make_request("GET", "links")
        if links:
            return links.get("Links", False)
        else:
            return False

    def get_transactions(self):
        """
        Return a list of Transaction from the accounts linked to your OnTrees account.
        :return: a list of Transactions
        """
        transactions = self._make_request("GET", "transactions")
        if transactions:
            return transactions.get("Transactions", False)
        else:
            return False

    def login(self):
        """
        Login to your OnTrees account. Doesn't have to called manually, but can be used to check that the
        provided credentials are valid. Returns True on success, False on failure
        :return: True on success, False on failure
        """

        # Check credentials were given
        if self._email is None or self._password is None:
            raise ValueError("Please provide an authentication email and password")

        # Make login request
        r = self._make_request("POST",
                               "users/login",
                               {"email": self._email, "password": self._password},
                               True)

        # If the login was successful
        if r is not False and r.get("Session"):
            self._auth_token = r.get("Session").get("BearerToken")
            return True

        # Otherwise, if the request was unsuccessful
        else:
            self._auth_token = None
            return False

    def start_refresh_linked_bank(self, linked_bank=None):
        """
        Sends a request to begin refreshing the given Linked Bank. Bank is not necessarily refreshed once
        this function has returned.
        :param linked_bank: a Linked Bank to refresh
        :return: True on success, False on failure
        """

        # If no link is given
        if linked_bank is None:
            return False

        # Only attempt refreshing if it's been over an hour since the link was refreshed
        last_refresh_timestamp = linked_bank.get("LastRefreshDate")
        if last_refresh_timestamp:
            last_refresh_time = datetime.strptime(last_refresh_timestamp, "%Y-%m-%dT%H:%M:%S.%f")
            if last_refresh_time + timedelta(hours=1) > datetime.utcnow():
                return 0

        # Build the refresh url
        link_url = "links/{0}/refresh".format(linked_bank.get("LinkId"))

        # Send the request
        return self._make_request("POST", link_url)

    def start_refresh_linked_banks(self, linked_banks=None):
        """
        Sends a request to begin refreshing the given list of Linked Banks. Banks are not necessarily refreshed once
        this function has returned.
        :param linked_banks: a list of Linked Banks. Can be omitted to have all Linked Banks refreshed
        :return: The number of Linked Banks that will be refreshed
        """

        # If no linked banks are given, retrieve them
        if linked_banks is None:
            linked_banks = self.get_linked_banks()

        # Init counter
        refresh_count = 0

        # Refresh all linked banks
        for linked_bank in linked_banks:
            refresh_count += 1 if self.start_refresh_linked_bank(linked_bank) else 0

        # Return count
        return refresh_count
