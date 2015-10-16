# OnTrees #
An unoffical module for interacting with the [OnTrees](https://www.ontrees.com) finance management service.

Allows you to retrieve a list of your linked banks, linked accounts. You can also refresh your account balances
and retrieve a list of past transactions (limited to 90 days)

## Installation ##
To install, just download the zip file, extract it and navigate to it.

Then run ```python setup.py install``` and you're done.

To get up and running quickly, edit ```ontrees_example.py``` to match your credentials and run ```python ontrees_example.py```

## Example ##
Here's a simple example that refreshes your account data and then lists your accounts and transactions.
```Python
from time import sleep

import ontrees

otc = ontrees.Client(email="YOUR_EMAIL", password="YOUR_PASSWORD")

print "Attempting to log in"
if otc.login():
    print "Login successful"
else:
    print "Login failed, please check your credentials. Aborting."
    exit()

print "Getting linked banks..."
linked_banks = otc.get_linked_banks()
if linked_banks:
    print "Found {0} linked banks(s)".format(len(linked_banks))
else:
    print "Request failed. Aborting"
    exit()

print "Refreshing accounts..."
refresh_count = otc.start_refresh_linked_banks(linked_banks)
print "{0} banks refreshed".format(refresh_count)

# wait 60 seconds if there are accounts being refreshed
if refresh_count > 0:
    print "Waiting 60 seconds to allow all banks to have been refreshed. " \
          "You could be cleverer than me here, by calling get_links() " \
          "and checking the LastRefreshTime but I'm okay with waiting."
    sleep(60)
    # Refresh linked banks
    linked_banks = otc.get_linked_banks()

# Print a list of accounts
accounts = otc.get_accounts(linked_banks)
print
print "Bank accounts:"
for account in accounts:
    print "{0} {1:9.2f} {2}".format(account.get("AccountNumber"),
                                    account.get("CurrentBalance"),
                                    account.get("AccountName"))

print
print "Getting transactions..."
transactions = otc.get_transactions()

if transactions:
    for transaction in transactions:
        print "{0} {1:7.2f} {2}".format(transaction.get("TransactionDate"),
                                        transaction.get("TransactionAmount"),
                                        transaction.get("Description"))
else:
    print "Request failed. Aborting"
    exit()
```

## API ##
###get_accounts###

Return a list of ```Accounts``` that are linked to your OnTrees account


###get_linked_banks###

Return a list of ```Linked Banks``` that are linked to your OnTrees account. A list of accounts can also be retrieved from here.


###get_transactions###

Return a list of ```Transaction``` from the accounts linked to your OnTrees account.


###login###

Login to your OnTrees account. Doesn't have to called manually, but can be used to check that the provided credentials are valid. Returns True on success, False on failure
        
        
###start_refresh_linked_bank###

Sends a request to begin refreshing the given ```Linked Bank```. ```Linked_Bank``` is not necessarily refreshed once this function has returned.
        
        
###start_refresh_linked_banks###

Sends a request to begin refreshing the given list of ```Linked Banks```. ```Linked_Banks``` are not necessarily refreshed once this function has returned.

## Schema ##
### Linked Bank ###
```
{
    "LinkId": 1234,
    "UserId": 1234,
    "PortalId": 1234,
    "AddedDate": "2015-01-01T00:00:00.000",
    "RefreshStatus": "Success",
    "RefreshStatusDate": "2015-01-01T00:00:00.000",
    "LastRefreshDate": "2015-01-01T00:00:00.000",
    "Portal": {
        "PortalId": 1234,
        "Name": "BankName",
        "ImageKey": "http://url",
        "LoginUrl": "https://login-url",
        "IsMfa": false,
        "IsBeta": false,
        "Type": "Banking"
    },
    "Accounts": [
        {ACCOUNT},
        {ACCOUNT}    
    ]
}
```

### Account ###
```
{
    "AccountId": 12345
    "AccountName": "Name",
    "OriginalAccountName": "Name",
    "AccountNumber": "xxxx1234",
    "AccountType": "checking",
    "CurrencyCode": "GBP",
    "CurrencySymbol": "£",
    "CurrentBalance": 9999,
    "AvailableBalance": 9999,
    "IsHidden": false
}
```

### Transaction ###
```
{
    "TransactionId": 1234,
    "AccountId": 1234,
    "CategoryId": 1234,
    "TransactionDate": "2015-01-01T00:00:00.000",
    "Description": "Description",
    "TransactionAmount": 1234,
    "ModifiedDate": "2015-01-01T00:00:00.000",
    "CurrencyCode": "GBP",
    "CurrencySymbol": "£",
    "OriginalDescription": "Description",
    "TransactionType": "credit"
}
```