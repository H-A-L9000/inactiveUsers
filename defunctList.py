"""
a script that identifies inactive users in slurmdb and provides their slurm associations/accounts as a dictionary
printed with pprint
"""

inactives = []
defunct = {}

showUsers = ['sacctmgr', '-P', '-n', 'show', 'user', 'format=User']
users = subprocess.run(showUsers, text=True, check=True, stdout=subprocess.PIPE).stdout.splitlines()

for user in users:
    try:
        user_info = pwd.getpwnam(user)
    except KeyError:
        inactives.append(user)
    else:
        shell = user_info.pw_shell

        if shell == "/bin/false":
            inactives.append(user)


for user in inactives:
        listAccounts = ['sacctmgr', '-P', '-n', 'show', 'assoc', 'user={}' .format(user), 'format=Account']
        listAcc=subprocess.run(listAccounts, text=True, stdout=subprocess.PIPE).stdout.splitlines()

        removeDup = []


        [removeDup.append(x) for x in listAcc if x not in removeDup]
        orderedAcc = sorted(removeDup)
        tuple(orderedAcc)

        defunct.update({user: orderedAcc})
        time.sleep(5)

print(len(defunct))
#print(len(list(defunct.keys())))
with open('defunct.txt', 'w') as outfile:
    pprint.pprint(defunct, outfile)
#pprint.PrettyPrinter(width=4).pprint(defunct)

