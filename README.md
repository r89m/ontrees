# OnTrees #
An unoffical module for interacting with the [OnTrees](https://www.ontrees.com) finance management service.

Allows you to retrieve a list of your linked banks, linked accounts. You can also refresh your account balances
and retrieve a list of past transactions (limited to 90 days)

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