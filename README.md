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
   to the `PtController` Apex class.

## Part 2: Use ptrunner.py to collect test results.

TODO