import psycopg2
from psycopg2.extensions import AsIs
from ultimatum_config import CONFIG
from ._builtin import Page

username = CONFIG['db_username']
password = CONFIG['db_password']
address = CONFIG['db_address']
schema_name = CONFIG['db_schema_name']
database_name = CONFIG['db_name']


########################## utility functions #############################

def store_players_thresholds(session_code, player_id, message, min_accept, max_reject):
    conn = psycopg2.connect(host=address, database=database_name, user=username, password=password)
    cur = conn.cursor()

    insert = """INSERT INTO %s.THRESHOLDS(
                                     SESSION_CODE, PLAYER_ID, MESSAGE, MIN_ACCEPT, MAX_REJECT)
                                     VALUES (%s, %s, %s, %s, %s );"""
    params = (
        AsIs(schema_name), session_code, AsIs(player_id), message, AsIs(min_accept), AsIs(max_reject),)

    try:
        cur.execute(insert, params)
        cur.close()
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


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
