
from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, Currency as c, currency_range
)

author = 'Roy Zerbib'


selfish_message = "we indicate that you will probably get a very selfish offer"
generous_message = "we indicate that you will probably get a very generous offer"
average_message = "we indicate that you will probably get an average offer"
messages = [selfish_message, generous_message, average_message]


class Constants(BaseConstants):
    name_in_url = 'choose_thresholds'
    players_per_group = None

    instructions_template = 'choose_thresholds/Instructions.html'

    num_rounds = len(messages)

    endowment = c(100)
    payoff_if_rejected = c(0)
    offer_increment = c(1)

    offer_choices = currency_range(0, endowment, offer_increment)
    offer_choices_count = len(offer_choices)


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.set_message()
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # the minimal amount the player would accept
    min_accept = models.CurrencyField(initial=0)

    # the maximal amount the player would reject
    max_reject = models.CurrencyField(initial=0)

    index = models.IntegerField(initial=0)

    # the message displayed to the player in 'complex' mode
    message = models.StringField(initial='')

    def set_message(self):
        if self.round_number > 1:
            self.index = self.in_round(self.round_number - 1).index + 1
        self.message = messages[self.index]

