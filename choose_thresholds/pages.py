from MySQLdb import Warning, Error, connect

from ultimatum_config import CONFIG
from ._builtin import Page

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


def create_tables():
    db = connect(address, username, password, schema_name)
    cursor = db.cursor()
    # create a table that stores the user'ss thresholds for each message
    if CONFIG['complex_mode']:
        query = """CREATE TABLE IF NOT EXISTS THRESHOLDS(
                                        SESSION_CODE  CHAR(30) NOT NULL,
                                        PLAYER_ID INT NOT NULL,
                                        MESSAGE CHAR(100),                                      
                                        MIN_ACCEPT INT NOT NULL,
                                        MAX_ACCEPT INT NOT NULL,
                                        CONSTRAINT PK_ROUND PRIMARY KEY (SESSION_CODE,PLAYER_ID,MESSAGE))
                                        """
        try:
            cursor.execute(query)
            db.commit()

        except (Error, Warning) as e:
            print(e)
            db.rollback()

    query = """CREATE TABLE IF NOT EXISTS ALL_DATA(
                                      SESSION_CODE  CHAR(30) NOT NULL,
                                      ROUND  INT NOT NULL,
                                      PLAYER_ID INT NOT NULL,
                                      COMPLEX CHAR(1) NOT NULL,
                                      MESSAGE CHAR(100),
                                      AMOUNT_OFFERED INT NOT NULL,
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


def store_players_thresholds(session_code, player_id, message, min_accept, max_accept):
    db = connect(address, username, password, schema_name)
    cursor = db.cursor()

    insert = """INSERT INTO THRESHOLDS(
                                 SESSION_CODE, PLAYER_ID, MESSAGE, MIN_ACCEPT, MAX_ACCEPT)
                                 VALUES (%s, %s, %s, %s, %s ) 
                                 """
    try:
        cursor.execute(insert, (session_code, player_id, message, min_accept, max_accept,))

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
        return self.round_number == 1

    def before_next_page(self):
        create_database()
        create_tables()


class ChooseThresholds(Page):
    form_model = 'player'
    form_fields = ['min', 'max']

    def is_displayed(self):
        return CONFIG['complex_mode']

    def before_next_page(self):
        if CONFIG['complex_mode']:
            session_code = self.session.__dict__['code']
            player_id = self.player.id_in_group
            message = self.player.message
            min_accept = currency_to_int(self.player.min)
            max_accept = currency_to_int(self.player.max)

            store_players_thresholds(session_code, player_id, message, min_accept, max_accept)


page_sequence = [
    Introduction,
    ChooseThresholds
]
