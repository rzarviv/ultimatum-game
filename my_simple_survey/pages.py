from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from game_config import GAMES
from .models import gameNum


def display_to_player_1(_self):
    return _self.participant.label == GAMES[gameNum]['p1']


def display_to_player_2(_self):
    return _self.participant.label == GAMES[gameNum]['p2']


class Instructions(Page):
    def is_displayed(self):
        return self.subsession.round_number <= 1

    pass


class Player1Choice(Page):
    form_model = 'group'
    form_fields = ['in_or_out']

    def is_displayed(self):
        return display_to_player_1(self)

    def vars_for_template(self):
        return {
            'f1': GAMES[gameNum]['f1'],
            's1': GAMES[gameNum]['s1'],
        }


class Player2Choice(Page):
    form_model = 'group'
    form_fields = ['left_or_right']

    def is_displayed(self):
        return (display_to_player_2(self)) and (self.group.in_or_out == 'In')

        # def before_next_page(self):

    def vars_for_template(self):
        return {
            'f2': GAMES[gameNum]['f2'],
            's2': GAMES[gameNum]['s2'],
            'f3': GAMES[gameNum]['f3'],
            's3': GAMES[gameNum]['s3'],
            'in_or_out': self.group.in_or_out
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        global gameNum
        gameNum = gameNum + 1
        pass


class Player1WaitPage(WaitPage):

    def is_displayed(self):
        return self.participant.label == GAMES[gameNum]['p2']


class Results(Page):
    pass


page_sequence = [
    #Instructions,
    Player1Choice,
    Player1WaitPage,
    Player2Choice,
    ResultsWaitPage,
    Results
]
