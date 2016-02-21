#!/usr/bin/env python2

from functools import partial

from soccersimulator import SoccerTeam, Player

import strategies
import potentialfield

_field = potentialfield.PotentialFields(
             potentialfield.FieldData(200, potentialfield.no_falloff),
             potentialfield.FieldData(150, potentialfield.no_falloff),
             potentialfield.FieldData(0, potentialfield.no_falloff),
             potentialfield.FieldData(0, potentialfield.no_falloff))

team1 = SoccerTeam("PotentialFields",
            [
                Player("PF1", strategies.PotentialFieldStrategy(_field))
            ])

team2 = SoccerTeam("PotentialFields",
            [
                Player("PF1", strategies.PotentialFieldStrategy(_field)),
                Player("PF2", strategies.PotentialFieldStrategy(_field))
            ])

team4 = SoccerTeam("PotentialFields",
            [
                Player("PF1", strategies.PotentialFieldStrategy(_field)),
                Player("PF2", strategies.PotentialFieldStrategy(_field)),
                Player("PF3", strategies.PotentialFieldStrategy(_field)),
                Player("PF4", strategies.PotentialFieldStrategy(_field))
            ])
