from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, Currency as c, currency_range
)
from MySQLdb import Warning, Error, connect
from ultimatum_config import CONFIG

author = 'Roy Zerbib'


# messages definition. add your messages here
# selfish_message = "we indicate that you will probably get a very selfish offer"
# generous_message = "we indicate that you will probably get a very generous offer"
# average_message = "we indicate that you will probably get an average offer"
# messages = [selfish_message, generous_message, average_message]
messages  = CONFIG['messages']

################################ database creation methods #######################################

username = CONFIG['db_username']
password = CONFIG['db_password']
address = CONFIG['db_address']
schema_name = CONFIG['db_schema_name']


def create_database():
    db = connect(address, username, password)
    cursor = db.cursor()
    query = 'CREATE DATABASE IF NOT EXISTS ' + schema_name

    try:
        cursor.execute(query)
        db.commit()

    except (Error, Warning) as e:
        print(e)
        db.rollback()

    db.close()


def create_table():
    db = connect(address, username, password, schema_name)
    cursor = db.cursor()
    # create a table that stores the user'ss thresholds for each message
    query = """CREATE TABLE IF NOT EXISTS THRESHOLDS(
                                           SESSION_CODE  CHAR(30) NOT NULL,
                                           PLAYER_ID INT NOT NULL,
                                           MESSAGE CHAR(100) NOT NULL,                                      
                                           MIN_ACCEPT INT NOT NULL,
                                           MAX_REJECT INT NOT NULL,
                                           CONSTRAINT PK_THRESHOLD PRIMARY KEY (SESSION_CODE,PLAYER_ID,MESSAGE))
                                           """
    try:
        cursor.execute(query)
        db.commit()

    except (Error, Warning) as e:
        print(e)
        db.rollback()

    db.close()

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
        create_table()

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
