from mdpsoccer import SoccerTeam,SoccerMatch

import os
import sys
import imp
import shutil
import argparse
import pickle

def dl_from_github(login,project,path):
    print("Debut import github %s %s" %(login,project))
    if not os.path.exists(path):
            os.mkdir(path)
    tmp_path=os.path.join(path,login)
    shutil.rmtree(tmp_path, ignore_errors=True)
    os.mkdir(tmp_path)
    os.system("git clone https://github.com/%s/%s %s " % (login,project,tmp_path))

def check_date(login,project,path):
    print login
    os.system("git --git-dir=%s/.git log  --format=\"%%Cgreen%%cd %%Creset \"| cut -d \" \" -f 1-3,7| uniq" %
            (os.path.join(path,login),))

def import_directory(tournament,path):
    path=os.path.realpath(path)
    logins=[login for login in os.listdir(path) if os.path.isdir(os.path.join(path,login))]
    for l in logins:
        tournament.add_club(load_club_directory(path,l))
    return tournament


def load_club_directory(path,login=None):
    projet=path
    if not login:
        projet,login=os.path.split(os.path.realpath(path))
    club_name = login
    try:
        sys.path.insert(0, projet)
        mymod = __import__(login)
        del sys.path[0]
    except Exception,e:
        print "\033[93m Erreur pour \033[94m%s : \033[91m%s \033[0m" % (club.login,str(e))
        print sys.exc_info()[0]
        return club
    print "Equipe de \033[92m%s\033[0m charge, \033[92m%s equipes\033[0m" % (login,len(mymod.teams))
    club.add_teams(mymod.teams)
    if hasattr(mymod,"name"):
        club.name=mymod.name
    return club


