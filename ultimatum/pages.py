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
    form_fields = ['right_reject', 'left_indifferent', 'right_indifferent', 'left_accept']

    def is_displayed(self):
        return self.round_number == 1
        # return self.player.id_in_group == 1 and self.round_number == 1

# TODO: change the error messages
    def error_message(self, values):
        # print('values are', values)
        msg = ""
        if values["left_indifferent"] < values["right_reject"]:
            msg += " 1"
        if values["left_accept"] < values["right_indifferent"]:
            msg += " 2"
        if msg != "":
            return msg
            # return 'The indifferent amount cannot be less than the reject amount'

    def before_next_page(self):
        print("left_indifferent :" + str(self.player.left_indifferent) +
              "left_accept :" + str(self.player.left_accept) +
              "right_indifferent :" + str(self.player.right_indifferent) +
              "right_reject" + str(self.player.right_reject))
        # self.player.reject = self.player.reject_interval
        # self.player.indifferent = self.player.indifferent_interval
        # print("reject interval is up to ", self.player.reject)
        # print("indifferent interval is up to ", self.player.indifferent)
        # print("reject interval is up to ", self.player.accept)


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
