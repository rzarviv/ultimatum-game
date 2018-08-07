from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from game_config import GAMES

author = 'Roy Zerbib'

doc = """
This is an extensive form game.
"""

gameNum = 0


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
    identity = models.StringField()
