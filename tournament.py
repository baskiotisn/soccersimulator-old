import os
import sys
import imp
import soccersimulator
import shutil


TARGET_PATH="/tmp/tournoi"
GIT_LIST=[("Benlog","Soccer-AI"),("SebXIII","Projet"),("andrenasturas","2I013"),("AlexandreCasanova","projet"),\
            ("mariene","projet_foot"),("Leynad","ProjetFoot"),("ArezkiSky","Projet-soccer-2I013")]

def load_git_list(git_import=True):
    tournament = Tournament("test")

    if git_import:
        print "Debut import github"
        if not os.path.exists(TARGET_PATH):
            os.mkdir(TARGET_PATH)
        for (login,mod) in GIT_LIST:
            tmp_path=os.path.join(TARGET_PATH,login)
            shutil.rmtree(tmp_path, ignore_errors=True)
            os.mkdir(tmp_path)
            os.system("git clone https://github.com/%s/%s %s " % (login,mod,tmp_path))
        print "Fin de l'import github"

    for (login,mod) in GIT_LIST:
        club  = SoccerClub(login)
        club.load_from_module()
        tournament.add_club(club)
    return tournament

class SoccerClub:
    def __init__(self,login=None):
        self.name=login
        self.teams=dict()
        self.login=login
        self._exceptions=[]

    def get_num_teams(self):
        return sum([ len(team) for team in self.teams.values()])

    def get_all_teams(self):
        return [x for i in self.teams.keys() for x in self.get_teams(i) ]
    def get_teams(self,i):
        if i in self.teams:
            return self.teams[i].values()
        return []
    def add_team(self,team):
        nbp = team.num_players
        if nbp not in self.teams:
            self.teams[nbp]=dict()
        if team.name not in self.teams[nbp]:
            self.teams[nbp][team.name]=team
            team.club=self

    def add_teams(self,teams):
        for team in teams:
            self.add_team(team)

    def load_from_module(self):
        try:
            sys.path.insert(0, TARGET_PATH)
            mymod = __import__(self.login)
            del sys.path[0]
        except Exception, e:
            print "Erreur pour %s : %s" % (self.login,str(e))
            self._exceptions.append(("Module %s " % (self.login,),e))
            return

        print "Equipe de %s charge, %s equipes" % (self.login,len(mymod.teams))
        self.add_teams(mymod.teams)
        if hasattr(mymod,"name"):
            self.name=mymod.name

    def __str__(self):
        return self.name



class Tournament:
    def __init__(self,name,same_club=False):
        self.clubs=[]
        self.name=name
        self.list_games=[1,2,4]
        self.battles=dict()
        self.battles_by_club=dict()
        self.same_club=same_club
    def add_club(self,club):
        self.clubs.append(club)

    def init_battles(self):
        self.battles=dict()
        self.battles_by_club=dict()
        for nbp in self.list_games:
            self.battles[nbp]=list()
            self.battles_by_club[nbp]=dict()
            for club in self.clubs:
                self.battles_by_club[nbp][club.login]=list()
        for club1 in range(len(self.clubs)):
            for club2 in range(club1+1 if not self.same_club else club1,len(self.clubs)):
                for nbp in self.list_games:
                    for team1 in self.clubs[club1].get_teams(nbp):
                        for team2 in self.clubs[club2].get_teams(nbp):
                            b = soccersimulator.SoccerBattle(team1,team2)
                            self.battles[nbp].append(b)
                            self.battles_by_club[nbp][self.clubs[club1].login].append(b)
                            self.battles_by_club[nbp][self.clubs[club2].login].append(b)
    def do_battles(self):
        for nbp in self.list_games:
            print "Tournoi %d joueurs" % (nbp,)
            for i,b in enumerate(self.battles[nbp]):
                b.run_multiple_battles(5,5000)
                print "Game ended %d/%d: %s" % (i,len(self.battles[nbp]),b)
