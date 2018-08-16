from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range,
)
import random
from settings import SESSION_CONFIGS

doc = """
Ultimatum game with two treatments: direct response and strategy method.
In the former, one player makes an offer and the other either accepts or rejects.
It comes in two flavors, with and without hypothetical questions about the second player's response to offers other than the one that is made.
In the latter treatment, the second player is given a list of all possible offers, and is asked which ones to accept or reject.
"""


class Constants(BaseConstants):
    name_in_url = 'ultimatum'
    players_per_group = None
    num_rounds = next((item for item in SESSION_CONFIGS if item["name"] == "ultimatum"), None)['num_rounds']

    instructions_template = 'ultimatum/Instructions.html'

    endowment = c(100)
    payoff_if_rejected = c(0)
    offer_increment = c(1)

    bad_offer_message = 'We think the offer is not good and you should reject it.'
    medium_offer_message = 'We think the offer is not so good, but not so bad.'
    good_offer_message = 'We think the offer is good and you should accept it.'
    messages = [good_offer_message, medium_offer_message, bad_offer_message]

    offer_choices = currency_range(0, endowment, offer_increment)
    offer_choices_count = len(offer_choices)

    keep_give_amounts = []
    for offer in offer_choices:
        keep_give_amounts.append((offer, endowment - offer))


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.amount_offered = random.choice(Constants.offer_choices)
            p.message = random.choice(Constants.messages)

            # randomize to treatments
            # for g in self.get_groups():
            #     g.amount_offered = random.choice(Constants.offer_choices)
            #     g.message = random.choice(Constants.messages)
            #
            #     if 'use_strategy_method' in self.session.config:
            #         g.use_strategy_method = self.session.config['use_strategy_method']
            #     else:
            #         g.use_strategy_method = random.choice([True, False])


def make_field(amount):
    return models.BooleanField(
        widget=widgets.RadioSelectHorizontal,
        label='Would you accept an offer of {}?'.format(c(amount)))


class Group(BaseGroup):
    use_strategy_method = models.BooleanField(
        doc="""Whether this group uses strategy method"""
    )

    # reject_interval = models.CurrencyField(choices=Constants.offer_choices)
    #
    # indifferent_interval = models.CurrencyField(choices=Constants.offer_choices)

    # amount_offered = models.CurrencyField(initial=random.choice(Constants.offer_choices))
    #
    # message = models.StringField(initial='')

    # for strategy method, see the make_field function above
    response_0 = make_field(0)
    response_10 = make_field(10)
    response_20 = make_field(20)
    response_30 = make_field(30)
    response_40 = make_field(40)
    response_50 = make_field(50)
    response_60 = make_field(60)
    response_70 = make_field(70)
    response_80 = make_field(80)
    response_90 = make_field(90)
    response_100 = make_field(100)

    def set_payoffs(self):
        # p1, p2 = self.get_players()
        # p1 = self.get_players()[0]

        # if self.use_strategy_method:
        #     self.offer_accepted = getattr(self, 'response_{}'.format(
        #         int(self.amount_offered)))

        for p in self.get_players():
            if p.offer_accepted:
                if self.round_number > 1:
                    # p1.payoff = (Constants.endowment - self.amount_offered) + p1.in_round(self.round_number - 1).payoff
                    p.payoff = p.amount_offered + p.in_round(self.round_number - 1).payoff
                    # p2.payoff = self.amount_offered + p2.in_round(self.round_number - 1).payoff
                else:
                    # p1.payoff = (Constants.endowment - self.amount_offered)
                    p.payoff = p.amount_offered
                    # p2.payoff = self.amount_offered
            else:
                if self.round_number > 1:
                    p.payoff = Constants.payoff_if_rejected + p.in_round(self.round_number - 1).payoff
                else:
                    p.payoff = Constants.payoff_if_rejected
                # p2.payoff = Constants.payoff_if_rejected


class Player(BasePlayer):
    payoff = models.CurrencyField(initial=0)
    reject = models.CurrencyField(initial=0)
    indifferent = models.CurrencyField(initial=0)
    accept = models.CurrencyField(initial=100)
    amount_offered = models.CurrencyField(initial=random.choice(Constants.offer_choices))
    message = models.StringField(initial='')
    reject_interval = models.CurrencyField(choices=Constants.offer_choices)
    indifferent_interval = models.CurrencyField(choices=Constants.offer_choices)
    offer_accepted = models.BooleanField(
        doc="if offered amount is accepted (direct response method)"
    )

    # left_reject = models.IntegerField()
    right_reject = models.IntegerField()
    left_indifferent = models.IntegerField()
    right_indifferent = models.IntegerField()
    left_accept = models.IntegerField()
    # right_accept = models.IntegerField()

    left = models.IntegerField()
    right = models.IntegerField()
