from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    # timeout_seconds = 600
    def is_displayed(self):
        return self.round_number == 1


class Offer(Page):
    form_model = 'player'
    form_fields = ['amount_offered']

    # def is_displayed(self):
    #     return self.player.id_in_group == 1

    # timeout_seconds = 600


class WaitForProposer(WaitPage):
    pass


class ChooseRanges(Page):
    form_model = 'player'
    form_fields = ['min_accept', 'max_reject']

    def is_displayed(self):
        return self.round_number == 1
        # return self.player.id_in_group == 1 and self.round_number == 1

    def error_message(self, values):
        # print('values are', values)
        if values["min_accept"] < values["max_reject"]:
            return "error"

    def before_next_page(self):
        print("min_accept :" + str(self.player.min_accept) +
              "max_reject :" + str(self.player.max_reject) +
              " sessions" + str(self.session.__dict__['code']))

        # put sql commands to store user's choices


class Accept(Page):
    form_model = 'player'
    form_fields = ['offer_accepted']

    # def is_displayed(self):
    #     return self.player.id_in_group == 1
    # return self.player.id_in_group == 2 and not self.group.use_strategy_method

    # timeout_seconds = 600

    def before_next_page(self):
        self.group.set_payoffs()


class AcceptStrategy(Page):
    form_model = 'group'
    form_fields = ['response_{}'.format(int(i)) for i in
                   Constants.offer_choices]

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.group.use_strategy_method


class Results(Page):
    pass


page_sequence = [Introduction,
                 ChooseRanges,
                 # Offer,
                 # WaitForProposer,
                 Accept,
                 # AcceptStrategy,
                 # ResultsWaitPage,
                 Results]
