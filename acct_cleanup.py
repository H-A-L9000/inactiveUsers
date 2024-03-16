#!/usr/bin/env python
import subprocess
import logging
import sys
import tempfile
import os
import time
import pwd
import argparse
import datetime
"""
a script that identifies inactive users in slurmdb 

inactive users can be removed using the command:
    sacctmgr remove user <username> cluster=<cluster>

implemented time.sleep function to prevent a degradation of performance 
more than 300 users are listed as inactive and too many remote calls from sacctmgr can result in DOS
"""

#@click.command()
#@click.option('--verbose', is_flag=True, help="Will print verbose message")
#@click.option('--write', is_flag=True, help="Apply changes to database")
#@click.option('--display', is_flag=True, help="Show current list of inactive users in slurmdb")


arg_parser= argparse.ArgumentParser()
arg_parser.add_argument('--cluster', required='--write' in sys.argv, help="cluster to execute on")
arg_parser.add_argument('--verbose', help="Will print verbose message", action='store_true')
arg_parser.add_argument('--write', help="Apply changes to database", action='store_true')
arg_parser.add_argument('--display', help="Show current list of inactive users in slurmdb", action='store_true')

args = arg_parser.parse_args(args=None if sys.argv[1:] else ['--help'])

inactives = []
timestamp = datetime.datetime.now().strftime("%Y-%m-%d")

def processUsers():
    with tempfile.TemporaryFile(mode='w+t') as tmp:
        try:
            showUsers = ['sacctmgr', '-P', '-n', 'show', 'user', 'format=User,DefaultAccount']
            subprocess.run(showUsers, stdout=tmp, text=True, check=True)
            if(os.stat(tmp.name).st_size == 0):
                sys.exit("User data file is empty")

            tmp.seek(0)

            for line in tmp:
                currentline = line.split('|')
                user = currentline[0]
                group = currentline[1]

                try:
                    user_info = pwd.getpwnam(user)
                except KeyError:
                    inactives.append(user)
                    #slurm account should probably not be touched
                    print("User",user, "not present in unix groups/passwd database")
                else:
                    shell = user_info.pw_shell

                    if shell == "/bin/false":
                        if args.display:
                            logUsers(user)
                        if args.write:
                            removeUsers(user)
                            time.sleep(3)
        finally:
            tmp.close()

def logUsers(user):
    inactives.append(user)
    file = open('inactive_users{}.txt'.format(timestamp) , 'w')
    for x in inactives:
        file.write(x+"\n")
    file.close()
