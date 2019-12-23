public with sharing class PerformLoopLocalVariableSingleUse
        implements Performable {

    public static final Integer DEFAULT_NUMBER_OF_ACCOUNTS = 100;
    
    public static final String NUMBER_OF_ACCOUNTS_PARAM = 'numberofaccounts';
    
    public PerformController.PerformSample execute(Map<String, String> context) {

        // Get the number of accounts for the test
        Integer numberOfAccounts = context.containsKey(NUMBER_OF_ACCOUNTS_PARAM)
                ? Integer.valueOf(context.get(NUMBER_OF_ACCOUNTS_PARAM))
                : DEFAULT_NUMBER_OF_ACCOUNTS;
        
        // Determine the employee count threshold, assuming the Employees
        // field holds the number of contacts for the account.
        // We want 200 contacts for the test.
        Integer employeeThreshold =
                (Integer)(200.0 / numberOfAccounts).round(RoundingMode.UP);

        // Set up the test
        Map<Id, Account> accountMap = new Map<Id, Account>([
            SELECT Id, OwnerId
            FROM Account
            WHERE NumberOfEmployees >= :employeeThreshold
            LIMIT :numberOfAccounts
        ]);

        System.assertEquals(
            numberOfAccounts,
            accountMap.size(),
            'accountMap size'
        );

        List<Contact> contactList = [
            SELECT Id, AccountId, OwnerId
            FROM Contact
            WHERE AccountId IN :accountMap.keySet()
            LIMIT 200
        ];

        System.assertEquals(200, contactList.size(), 'contactList size');

        // Note the start time
        Datetime startDatetime = Datetime.now();

        for (Contact eachContact : contactList) {
            Account contactAccount = accountMap.get(eachContact.AccountId);
            eachContact.OwnerId = contactAccount.OwnerId;
        }

        // Note the stop time
        Datetime stopDatetime = Datetime.now();

        return new PerformController.PerformSample(
            stopDatetime.getTime() - startDatetime.getTime(),
            Datetime.now()
        );
    }
}