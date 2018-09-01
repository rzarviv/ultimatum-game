from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import MySQLdb as sql
import datetime

username = 'root'
password = 'royzerbib10'

# TODO: fix the pages' view according to kobi's mail : COMPLEX configuration (with message).
# There are x types of messages (for now let's say 2 types). Message 1 : You will get a selfish offer. Message 2: You will get a kind offer.
# Phase 1 and phase 2 adapt to the message. For example
#
# Input your strategy.
#
# For the message :  You will get a selfish offer., please input
# What is the smallest offer you would ABSOLUTELY accept?
#
# etc...

class Introduction(Page):
    # timeout_seconds = 600
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):

        db = sql.connect("localhost", username, password)
        cursor = db.cursor()
        create_database = 'CREATE DATABASE IF NOT EXISTS usersData'

        try:
            cursor.execute(create_database)
            db.commit()

        except (sql.Error, sql.Warning) as e:
            print(e)
            db.rollback()

        db.close()
        db = sql.connect("localhost", username, password, "usersData")
        cursor = db.cursor()
        create_table = """CREATE TABLE IF NOT EXISTS ALL_DATA(
                          SESSION_CODE  CHAR(30) NOT NULL,
                          ROUND  INT NOT NULL,
                          PLAYER_ID INT NOT NULL,
                          COMPLEX CHAR(1) NOT NULL,
                          MIN_ACCEPT INT NOT NULL,
                          MAX_REJECT INT NOT NULL,
                          AMOUNT_OFFERED INT NOT NULL,
                          MESSAGE CHAR(100),
                          OFFER_ACCEPTED CHAR(1) NOT NULL,
                          TIME_STAMP TIMESTAMP NOT NULL,
                          CONSTRAINT PK_ROUND PRIMARY KEY (SESSION_CODE,ROUND,PLAYER_ID))
                          """
        try:
            cursor.execute(create_table)
            db.commit()

        except (sql.Error, sql.Warning) as e:
            print(e)
            db.rollback()


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
        pass
        # print("min_accept :" + str(self.player.min_accept) +
        #       "max_reject :" + str(self.player.max_reject) +
        #       " sessions" + str(self.session.__dict__['code']))


class Accept(Page):
    form_model = 'player'
    form_fields = ['offer_accepted']

    # def is_displayed(self):
    #     return self.player.id_in_group == 1
    # return self.player.id_in_group == 2 and not self.group.use_strategy_method

    # timeout_seconds = 600

    def before_next_page(self):
        session_code = self.session.__dict__['code']
        round_num = self.round_number
        player_id = self.player.id_in_group

        if self.player.complex_mode:
            is_complex = 'Y'
        else:
            is_complex = 'N'

        if self.round_number > 1:
            self.player.max_reject = self.player.in_round(round_num - 1).max_reject
            self.player.min_accept = self.player.in_round(round_num - 1).min_accept

        min_accept = int(str(self.player.min_accept)[:-7].replace(' ', ''))
        max_reject = int(str(self.player.max_reject)[:-7].replace(' ', ''))
        amount_offered = int(str(self.player.amount_offered)[:-7].replace(' ', ''))
        message = self.player.message

        if self.player.offer_accepted:
            offer_accepted = str('Y')
        else:
            offer_accepted = str('N')

        time_stamp = str(datetime.datetime.utcnow())

        db = sql.connect("localhost", username, password, "usersData")
        cursor = db.cursor()
        insert = """INSERT INTO ALL_DATA(
                         SESSION_CODE, ROUND, PLAYER_ID, COMPLEX, MIN_ACCEPT, MAX_REJECT, AMOUNT_OFFERED, MESSAGE, OFFER_ACCEPTED, TIME_STAMP)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s ) 
                         """
        try:
            cursor.execute(insert, (
                session_code, round_num, player_id, is_complex, min_accept, max_reject, amount_offered, message,
                offer_accepted, time_stamp,))
            db.commit()
        except(sql.Error, sql.Warning) as e:
            print(e)
            db.rollback()

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
