from os import environ
from ultimatum_config import CONFIG

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'complex_mode': True,
    'doc': "In complex mode a random message is displayed to the player in every level of the game, indicates the "
           "system's opinion about the offer proposed to the player.",

}

SESSION_CONFIGS = [
    {
        'name': 'ultimatum_strategy_before_game',
        'display_name': "Ultimatum Game - strategy before game",
        'num_demo_participants': 1,
        'app_sequence': ['choose_thresholds', 'ultimatum'],
    },
    {
        'name': 'ultimatum_game_before_strategy',
        'display_name': "Ultimatum Game - game before strategy",
        'num_demo_participants': 1,
        'app_sequence': ['ultimatum', 'choose_thresholds'],
    },
    # other session configs go here ...
]
# see the end of this file for the inactive session configs


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    {
        'name': 'ultimatum',
        'display_name': 'Room for ultimatum game',
    },
]

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = 'STUDY'  # environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = CONFIG['admin_username']

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = CONFIG['admin_password']  # environ.get('OTREE_ADMIN_PASSWORD')

# Consider '', None, and '0' to be empty/false
# DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})
DEBUG = False

DEMO_PAGE_INTRO_HTML = """
Here are various games implemented with 
oTree. These games are open
source, and you can modify them as you wish.
"""

# don't share this with anybody.
SECRET_KEY = '5!sx)cs(uhcjfga+5__&8x$r+6%kywask0iq9*(q#4d8)0lcw3'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

environ['DATABASE_URL'] = 'postgres://postgres@localhost/ultimatum'


# environ['DATABASE_URL'] = 'mysql://localhost:3306'
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': CONFIG['db_schema_name'],
#         'USER': CONFIG['db_username'],
#         'PASSWORD': CONFIG['db_password'],
#         'HOST': CONFIG['db_address'],
#         'PORT': '3306',
#     }
# }

# DATABASES = {
#         'default': {
#             'HOST': 'localhost',
#             'PORT': '3306',
#             'ENGINE': 'mysql.connector.django',
#             'NAME': 'usersdata',
#             'USER': 'root',
#             'PASSWORD': 'royzerbib10'
#         }
#     }


# {
#     'name': 'my_simple_survey',
#     'num_demo_participants': 4,
#     'app_sequence': ['my_simple_survey'],
#     # 'num_rounds':  len(GAMES),# this attribute was added to the 'Configure Session' segment in both 'sessions' and 'room' pages
# },
