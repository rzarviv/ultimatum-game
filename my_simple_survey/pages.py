from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    pass


class Player1_Choice(Page):
    form_model = 'group'
    form_fields = ['f1', 's1', 'in_or_out']
    pass


class Player2_Choice(Page):
    form_model = 'group'
    form_fields = ['f2', 's2', 'f3', 's3', 'left_or_right']
    pass


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    Instructions,
    Player1_Choice,
    Player2_Choice,
    # ResultsWaitPage,
    Results
]
