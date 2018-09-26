from ._builtin import Page
from MySQLdb import Warning, Error, connect
import datetime
from ultimatum_config import CONFIG
from .models import Constants

username = CONFIG['db_username']
password = CONFIG['db_password']
schema_name = CONFIG['db_schema_name']
address = CONFIG['db_address']


########################## utility functions #############################

def store_players_data(session_code, round_num, player_id,
                       is_complex, amount_offered, message, offer_accepted, time_stamp):
    db = connect(address, username, password, schema_name)
    cursor = db.cursor()
    insert = """INSERT INTO ALL_DATA(
                                 SESSION_CODE, ROUND, PLAYER_ID, COMPLEX, AMOUNT_OFFERED, MESSAGE, OFFER_ACCEPTED, TIME_STAMP)
                                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s ) 
                                 """
    try:
        cursor.execute(insert, (
            session_code, round_num, player_id, is_complex, amount_offered, message,
            offer_accepted, time_stamp,))

        db.commit()
    except(Error, Warning) as e:
        print(e)
        db.rollback()

    db.close()


def currency_to_int(currency_field):
    #  removes the ' points' suffix from the currency's string representation and converts it to int
    return int(str(currency_field)[:-7])


#########################################################################


class Introduction(Page):
    def is_displayed(self):
        if self.session.__dict__['config']['name'] == "ultimatum_strategy_before_game":
            return False
        else:
            return self.round_number == 1

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

        self.player.set_total_amount_offered()

        self.player.current_endowment = round_num * Constants.endowment

        message = self.player.message

        if self.player.offer_accepted:
            offer_accepted = 'Y'
        else:
            offer_accepted = 'N'

        time_stamp = str(datetime.datetime.utcnow())

        store_players_data(session_code, round_num, player_id, is_complex, amount_offered,
                           message, offer_accepted, time_stamp)

        self.player.set_payoff()


class Results(Page):
    def is_displayed(self):
        if self.player.complex_mode:
            return self.round_number == Constants.num_rounds
        else:
            return True


page_sequence = [Introduction,
                 Accept,
                 Results]
