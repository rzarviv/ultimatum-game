from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range,
)
import random
from ultimatum_config import CONFIG


class Constants(BaseConstants):
    name_in_url = 'ultimatum'

    # only one player is in a group
    players_per_group = None

    # the number of rounds is configured in 'ultimatum_config.py'
    num_rounds = CONFIG['num_rounds']

    instructions_template = 'ultimatum/Instructions.html'
    popup_template = 'ultimatum/PopupMessage.html'

    #  maximal amount that can be offered to a player
    endowment = c(100)

    payoff_if_rejected = c(0)
    offer_increment = c(1)

    selfish_message = "Our system indicates that you'll probably get a very selfish offer."
    generous_message = "Our system indicates that you'll probably get a very generous offer."
    average_message = "Our system indicates that you'll probably get an average offer."
    messages = [selfish_message, generous_message, average_message]

    #  range of all the offers a player can get
    offer_choices = currency_range(0, endowment, offer_increment)
    offer_choices_count = len(offer_choices)


class Subsession(BaseSubsession):

    # if the app has multiple rounds, creating_session gets run multiple times consecutively
    def creating_session(self):
        for p in self.get_players():
            p.amount_offered = random.choice(Constants.offer_choices)
            p.complex_mode = CONFIG['complex_mode']
            p.set_message()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # the player's total payoff in all rounds
    payoff = models.CurrencyField(initial=0)

    # the amount that is offered for each player
    amount_offered = models.CurrencyField(initial=random.choice(Constants.offer_choices))

    # the message displayed to the player in 'complex' mode
    message = models.StringField(initial='')

    # indicates if the offer was accepted or not
    offer_accepted = models.BooleanField()

    # the minimal amount the player would accept
    min_accept = models.CurrencyField(initial=0)

    # the maximal amount the player would reject
    max_reject = models.CurrencyField(initial=0)

    # indicates if the 'complex' mode is on or not
    complex_mode = models.BooleanField(initial=0)

    def set_payoff(self):
        if self.offer_accepted:
            if self.round_number > 1:
                self.payoff = self.amount_offered + self.in_round(self.round_number - 1).payoff
            else:
                self.payoff = self.amount_offered
        else:  # offer rejected
            if self.round_number > 1:
                self.payoff = Constants.payoff_if_rejected + self.in_round(self.round_number - 1).payoff
            else:
                self.payoff = Constants.payoff_if_rejected

    def set_message(self):
        if self.complex_mode:
            self.message = random.choice(Constants.messages)
