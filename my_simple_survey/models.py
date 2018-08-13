from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
)

from game_config import GAMES

author = 'Roy Zerbib'

doc = """
This is an extensive form game.
"""

gameNum = 0
currentGame = GAMES[gameNum]


class Constants(BaseConstants):
    name_in_url = 'my_simple_survey'
    players_per_group = 2
    num_rounds = len(GAMES)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    f1 = models.IntegerField(label=GAMES[gameNum]['f1'])
    s1 = models.IntegerField(label=GAMES[gameNum]['s1'])
    f2 = models.IntegerField(label=GAMES[gameNum]['f2'])
    s2 = models.IntegerField(label=GAMES[gameNum]['s2'])
    f3 = models.IntegerField(label=GAMES[gameNum]['f3'])
    s3 = models.IntegerField(label=GAMES[gameNum]['s3'])

    in_or_out = models.StringField(
        choices=['In', 'Out'],
        widget=widgets.RadioSelect
    )

    left_or_right = models.StringField(
        choices=['Left', 'Right'],
        widget=widgets.RadioSelect
    )


class Player(BasePlayer):
    # identity = models.StringField()
    total_points = models.IntegerField()

    def role(self):
        if self.participant.label == GAMES[gameNum]['p1'] :
            return 'bidder'
        else:
            return 'responder'

    def get_partner(self):
        return self.get_others_in_group()[0]

    def add_points(self,points):
        self.total_points += points