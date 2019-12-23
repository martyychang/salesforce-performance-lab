# Salesforce Performance Lab

This app helps developers assess the effectiveness of their code and
determine which development practices to adopt for superior performance,
meaning shorter runtimes and heap sizes.

## Part 1: Create a scratch org.

The safest place to run the tests are in a scratch org.

```bash
sfdx force:org:create -f config/project-scratch-def.json -s
sfdx force:source:push
```

Next are a few required manual steps.

1. Create a Force.com Site named "Public" with the root web address.
   For the subdomain, simply use the unique portion of
   your scratch org subdomain, such as "dream-connect-9323".
2. Set the Active Site Home Page to "UnderConstruction".
3. Activate the site.
4. Edit Public Access Settings for the site, and grant the site access
   to the `PerformController` Apex class.

And you'll probably want some test data. Below is some anonymous Apex
you can run to create 200 accounts and 1,286 contacts.

```java
// Initialize the lists of accounts and contacts
List<Account> accountList = new List<Account>();
List<Contact> contactList = new List<Contact>();

// Create the accounts and each one's associated contacts
for (Decimal i = 1; i <= 200; i++) {
    Account newAccount = new Account(
        Description = 'It would take no more than ' + i
                + ' of these companies to collect 200 contacts',
        Name = 'Company ' + i,
        NumberOfEmployees = (Integer)(200.0 / i).round(RoundingMode.UP)
    );
    
    accountList.add(newAccount);
    
    for (Decimal j = 1; j <= newAccount.NumberOfEmployees; j++) {

        // We store the account on the contact, so that later
        // we can loop through the contacts and populate the actual
        // `AccountId`. Populating just `Account` did not seem to be
        // enough to establsh the relationship.
        Contact newContact = new Contact(
			      Account = newAccount,
            Email = 'person' + j + '@' + i + '.example.company',
            FirstName = 'Person ' + j,
            LastName = 'of ' + newAccount.NumberOfEmployees
        );
        
        contactList.add(newContact);
    }
}

// Create the accounts
insert accountList;

// Populate `Contact.AccountId` using the now-available Account ID values.
for (Contact eachContact : contactList) {
    eachContact.AccountId = eachContact.Account.Id;
}

// Create the contacts
insert contactList;
```

## Part 2: Use runner.py to collect test results.

Once the API is set up, you can use **bin/runner.py** to collect results
that will be stored in the **.runner/out** directory
within your local project.

```bash
# This will collect 10 samples and store them inside a local file:
# .runner/out/PerformLoopLocalVariableSingleUse.csv
python3 bin/runner.py \
    -t PerformLoopLocalVariableSingleUse \
    -n 10 \
    -r http://sandbox-drive-velocity-1634-developer-edition.cs1.force.com
```

There are system limits in Salesforce that make retrieving a large number
of results rather difficult. To work around this, without having to write
crazy code to handle the logic in Salesforce, simply use a loop within
the command line.

```bash
# This command in Bash will effectively run until 1,000 samples are collected.
#
# See details: https://serverfault.com/a/737269
seq 100 | xargs -I -- python3 bin/runner.py \
    -t PerformLoopMapItemSingleUse \
    -n 10 \
    -r http://sandbox-drive-velocity-1634-developer-edition.cs1.force.com
```
