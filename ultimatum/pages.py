from ._builtin import Page
from MySQLdb import Warning, Error, connect
import datetime
from ultimatum_config import CONFIG
from .models import Constants

username = CONFIG['db_username']
password = CONFIG['db_password']
schema_name = CONFIG['db_schema_name']
address = CONFIG['db_address']


# ----------------------------utility functions-------------------- #
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

    db.close()  # closing now to connect to the new database later


def create_table():
    db = connect(address, username, password, schema_name)
    cursor = db.cursor()
    query = """CREATE TABLE IF NOT EXISTS ALL_DATA(
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
        cursor.execute(query)
        db.commit()

    except (Error, Warning) as e:
        print(e)
        db.rollback()

    db.close()


def store_players_data(session_code, round_num, player_id,
                       is_complex, min_accept, max_reject,
                       amount_offered, message, offer_accepted, time_stamp):
    db = connect(address, username, password, schema_name)
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
    except(Error, Warning) as e:
        print(e)
        db.rollback()

    db.close()


def currency_to_int(currency_field):
    #  removes the ' points' suffix from the currency's string representation and converts it to int
    return int(str(currency_field)[:-7])


# ----------------------------endof utility functions-------------------- #


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        self.player.set_message()
        create_database()
        create_table()


# class Offer(Page):
#     form_model = 'player'
#     form_fields = ['amount_offered']


class ChooseRanges(Page):
    form_model = 'player'
    form_fields = ['min_accept', 'max_reject']

    def is_displayed(self):
        return self.round_number == 1

    def error_message(self, values):
        if values["min_accept"] < values["max_reject"]:
            return "the minimal amount you'd absolutely accept cannot be less than the maximal amount you'd " \
                   "absolutely reject "

    def before_next_page(self):
        self.player.set_message()


class Accept(Page):
    form_model = 'player'
    form_fields = ['offer_accepted']

    def before_next_page(self):
        # each session has a unique code which is stored in the session's dictionary
        session_code = self.session.__dict__['code']

        round_num = self.round_number
        player_id = self.player.id_in_group

        if self.player.complex_mode:
            is_complex = 'Y'
        else:
            is_complex = 'N'

        amount_offered = currency_to_int(self.player.amount_offered)

        # reserve the min_accept and max_reject attributes that getting zeroed in every round.
        self.player.reserve_min_max()
        self.player.set_total_amount_offered()

        self.player.total_endowment = round_num * Constants.endowment

        # if self.round_number > 1:
        #     self.player.max_reject = self.player.in_round(round_num - 1).max_reject
        #     self.player.min_accept = self.player.in_round(round_num - 1).min_accept

        min_accept = currency_to_int(self.player.min_accept)
        max_reject = currency_to_int(self.player.max_reject)

        message = self.player.message

        if self.player.offer_accepted:
            offer_accepted = 'Y'
        else:
            offer_accepted = 'N'

        time_stamp = str(datetime.datetime.utcnow())

        store_players_data(session_code, round_num, player_id, is_complex, min_accept, max_reject, amount_offered,
                           message,
                           offer_accepted, time_stamp)

        self.player.set_payoff()


class Results(Page):
    def is_displayed(self):
        if self.player.complex_mode:
            return self.round_number == CONFIG['num_rounds']
        else:
            return True


page_sequence = [Introduction,
                 ChooseRanges,
                 Accept,
                 Results]
