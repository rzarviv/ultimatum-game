from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, Currency as c, currency_range
)
import psycopg2
from psycopg2.extensions import AsIs

from ultimatum_config import CONFIG

author = 'Roy Zerbib'

messages = CONFIG['messages']

################################ database creation methods #######################################

username = CONFIG['db_username']
password = CONFIG['db_password']
address = CONFIG['db_address']
schema_name = CONFIG['db_schema_name']
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
        print(str(error))
    finally:
        if conn is not None:
            conn.close()


def create_table_thresholds():
    conn = psycopg2.connect(host=address, database=database_name, user=username, password=password)
    cur = conn.cursor()
    command = """ CREATE TABLE IF NOT EXISTS %s.THRESHOLDS (
                                            SESSION_CODE VARCHAR(30) NOT NULL,
                                            PLAYER_ID INTEGER NOT NULL,
                                            MESSAGE VARCHAR(100) NOT NULL,
                                            MIN_ACCEPT INTEGER NOT NULL,
                                            MAX_REJECT INTEGER NOT NULL,
                                            PRIMARY KEY (SESSION_CODE,PLAYER_ID,MESSAGE)
                                            ); """
    param = (AsIs(schema_name),)

    try:
        cur.execute(command, param)
        cur.close()
        conn.commit()
    except Exception as error:
        print(str(error))
    finally:
        if conn is not None:
            conn.close()


##################################################################################################


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

    # if the app has multiple rounds, creating_session gets run multiple times consecutively
    def creating_session(self):
        create_database()
        create_table_thresholds()

        for p in self.get_players():
            p.set_message()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # the minimal amount the player would accept
    min_accept = models.CurrencyField(initial=0)

    # the maximal amount the player would reject
    max_reject = models.CurrencyField(initial=0)

    # the number of message that is displayed to the player
    index = models.IntegerField(initial=0)

    # the message displayed to the player in 'complex' mode
    message = models.StringField(initial='')

    def set_message(self):
        # setting the next message that will be displayed to the player in 'complex_mode'.
        if self.round_number > 1:
            # incrementing the index by one.
            self.index = self.in_round(self.round_number - 1).index + 1
        self.message = messages[self.index]
