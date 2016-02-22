#from login2015 import liste_login
import argparse
from soccersimulator import SoccerTournament,SoccerTeam,SoccerMatch
from soccersimulator.scripts import *
import datetime

defaultpath="/tmp/proj2015/"


if __name__=="__main__":
    parse = argparse.ArgumentParser(description="Soccersimulator Main")
    parse.add_argument('-path',action='store',default=defaultpath,help="Import directory DIR")
    parse.add_argument('-git',action='store_true',default=False,help="Import github to directory")
    parse.add_argument('-noplay',action="store_true",default=False,help="Don't play the games")
    parse.add_argument('-steps', action="store",dest='max_steps',type=int,default=2000,help="Max steps")
    parse.add_argument('-nbp',nargs='+',type=int,help="List of type of tournament (number of player, 1,2 or 4)")
    parse.add_argument('-login',nargs='+',default=None,help='List of logins to play')
    parse.add_argument('-nosave',action="store_true",default=False,help="Don't save scores and matches")
    parse.add_argument('-replay',action="store",help="Watch replay")
    parse.add_argument('-nowatch',action="store_true",default=False,help="Don't watch live")
    parse.add_argument('-noretour',action="store_true",default=False,help="Play 1 side matches")
    parse.add_argument('-date',action="store_true",default=False)
    args=parse.parse_args()
    path = args.path
    print path
    fname = str(datetime.datetime.now()).replace("-","").split(" ")[0]
    nb_tournois = args.nbp if args.nbp else [1,2,4]

    if args.replay:
        tournoi = None
        try:
            tournoi = SoccerTournament.load(args.replay)
            print("Tournoi charge")
            print(tournoi.format_scores())
        except:
            pass
        if tournoi is None:
            try:
                tournoi = SoccerMatch.load(args.replay)
                print("Match charge")
            except:
                pass
        if tournoi is None:
            print("Format non reconnu")
        else:
            show(tournoi)
        sys.exit(0)

    if args.git:
        dl_from_github(liste_login,path)
    if args.date:
        check_date(liste_login,path)
    tournois = dict()
    for t in nb_tournois:
        tournois[t] = SoccerTournament(max_steps=args.max_steps,nb_players=t,retour=args.noretour)
    teams=import_directory(path)
    if not args.noplay:
        for k in tournois:
            for t in teams[k]:
                if not args.login or t in args.login:
                    if not tournois[k].add_team(t):
                        print "Equipe %s non ajoute, probleme de joueurs (%d joueurs, tournoi de %d)" % (t,t.nb_players,k)
        for k in tournois:
            if not args.nowatch:
                show(tournois[k])
            else:
                tournois[k].play(True)
            print tournois[k].format_scores()
            if not args.nosave:
                tournois[k].save(os.path.join(path,"res_%s_%d.trnmt" %(fname,k)))
