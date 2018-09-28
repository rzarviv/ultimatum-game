from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range,
)
import random
import psycopg2
from psycopg2.extensions import AsIs
from ultimatum_config import CONFIG

################################ database creation methods #######################################

username = CONFIG['db_username']
password = CONFIG['db_password']
schema_name = CONFIG['db_schema_name']
address = CONFIG['db_address']
database_name = CONFIG['db_name']


def create_database():
    conn = psycopg2.connect(host=address, database=database_name, user=username, password=password)
    cur = conn.cursor()
    command = """ CREATE SCHEMA IF NOT EXISTS %s AUTHORIZATION %s ;"""
    params = (AsIs(schema_name), AsIs(username),)

    try:
        cur.execute(command, params)
        cur.close()
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_table_all_data():
    conn = psycopg2.connect(host=address, database=database_name, user=username, password=password)
    cur = conn.cursor()
    command = """ CREATE TABLE IF NOT EXISTS %s.ALL_DATA (
                                                SESSION_CODE VARCHAR(30) NOT NULL,
                                                ROUND INTEGER NOT NULL,
                                                PLAYER_ID INTEGER NOT NULL,
                                                COMPLEX VARCHAR(1) NOT NULL,
                                                MESSAGE VARCHAR(100) NOT NULL,
                                                AMOUNT_OFFERED INTEGER NOT NULL,
                                                OFFER_ACCEPTED VARCHAR(1) NOT NULL,
                                                TIME_STAMP TIMESTAMPTZ NOT NULL,
                                                PRIMARY KEY (SESSION_CODE,ROUND,PLAYER_ID)
                                                ); """
    param = (AsIs(schema_name),)

    try:
        cur.execute(command, param)
        cur.close()
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


##################################################################################################

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

    selfish_message = "We indicate that you will probably get a very selfish offer"
    generous_message = "We indicate that you will probably get a very generous offer"
    average_message = "We indicate that you will probably get an average offer"
    messages = [selfish_message, generous_message, average_message]

    #  range of all the offers a player can get
    offer_choices = currency_range(0, endowment, offer_increment)
    offer_choices_count = len(offer_choices)


class Subsession(BaseSubsession):

    # if the app has multiple rounds, creating_session gets run multiple times consecutively
    def creating_session(self):
        create_database()
        create_table_all_data()
        for p in self.get_players():
            p.amount_offered = random.choice(Constants.offer_choices)
            p.complex_mode = self.session.config['complex_mode']
            p.set_message()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # the player's total payoff in all rounds
    payoff = models.CurrencyField(initial=0)

    # the amount that is offered for each player in every round
    amount_offered = models.CurrencyField(initial=0)

    total_amount_offered = models.CurrencyField(initial=0)

    # the total number of points the proposer and the divider had to divide between themselves.
    # usually, current_endowment = round_number * endowment
    current_endowment = models.CurrencyField(initial=0)

    # the message displayed to the player in 'complex' mode
    message = models.StringField(initial='')

    # indicates if the offer was accepted or not
    offer_accepted = models.BooleanField()

    # indicates if the 'complex' mode is on or not
    complex_mode = models.BooleanField(initial=False)

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

    def set_total_amount_offered(self):
        if self.round_number > 1:
            self.total_amount_offered = self.amount_offered + self.in_round(self.round_number - 1).total_amount_offered
        else:
            self.total_amount_offered = self.amount_offered

    def set_message(self):
        if self.complex_mode:
            self.message = random.choice(Constants.messages)
