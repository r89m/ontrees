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
          "You could be cleverer than me here, by calling get_links() and checking the LastRefreshTime " \
          "but I'm okay with waiting."
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
