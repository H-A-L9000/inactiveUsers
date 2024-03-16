# inactiveUsers

Retreiving a list of inactive user accounts that are still listed with an association in SLURM. The desired output will include the full user name along with the project the account has as association with.  An example output is:

User.Name,project

To determine if an account is inactive, use `getent passwd` and check the account's login shell.  

Some users may not be in the unix passwd database which raises errors when parsing the full list of users in slurm. 
