from MySQLdb import Warning, Error, connect

from ultimatum_config import CONFIG
from ._builtin import Page

username = CONFIG['db_username']
password = CONFIG['db_password']
address = CONFIG['db_address']
schema_name = CONFIG['db_schema_name']


########################## utility functions #############################

def store_players_thresholds(session_code, player_id, message, min_accept, max_reject):
    db = connect(address, username, password, schema_name)
    cursor = db.cursor()

    insert = """INSERT INTO THRESHOLDS(
                                 SESSION_CODE, PLAYER_ID, MESSAGE, MIN_ACCEPT, MAX_REJECT)
                                 VALUES (%s, %s, %s, %s, %s ) 
                                 """
    try:
        cursor.execute(insert, (session_code, player_id, message, min_accept, max_reject,))

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
        if self.session.__dict__['config']['name'] == "ultimatum_game_before_strategy":
            return False
        else:
            return self.round_number == 1


class ChooseThresholds(Page):
    form_model = 'player'
    form_fields = ['min_accept', 'max_reject']

    def before_next_page(self):
        session_code = self.session.__dict__['code']
        player_id = self.player.id_in_group
        message = self.player.message
        min_accept = currency_to_int(self.player.min_accept)
        max_reject = currency_to_int(self.player.max_reject)

        store_players_thresholds(session_code, player_id, message, min_accept, max_reject)


page_sequence = [
    Introduction,
    ChooseThresholds
]
