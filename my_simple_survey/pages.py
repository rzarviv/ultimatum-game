from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import roundNum
from game_config import GAMES


class Instructions(Page):
    def is_displayed(self):
        return self.subsession.round_number <= 1

    pass


class Player1_Choice(Page):
    form_model = 'group'
    form_fields = ['in_or_out']

    def is_displayed(self):
        return self.participant.label == GAMES[roundNum]['p1']

    def vars_for_template(self):
        return {
            'f1': GAMES[roundNum]['f1'],
            's1': GAMES[roundNum]['s1'],
        }


class Player2_Choice(Page):
    form_model = 'group'
    form_fields = ['left_or_right']

    def is_displayed(self):
        return self.participant.label == GAMES[roundNum]['p2']

    #def before_next_page(self):

    def vars_for_template(self):
        return {
            'f2': GAMES[roundNum]['f2'],
            's2': GAMES[roundNum]['s2'],
            'f3': GAMES[roundNum]['f3'],
            's3': GAMES[roundNum]['s3'],
        }


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        global roundNum
        roundNum = roundNum + 1
        pass


class Results(Page):
    def after_all_players_arrive(self):
        pass


page_sequence = [
    Instructions,
    Player1_Choice,
    Player2_Choice,
    ResultsWaitPage,
    Results
]
