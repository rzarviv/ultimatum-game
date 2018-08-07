

__PLAYERS_NAMES_FILENAME__ = 'game_subjects.txt'

SUBJECTS_ID = [line.rstrip('\n') for line in open(__PLAYERS_NAMES_FILENAME__)]

# p1 is the bidder, p2 is the responder
GAMES = [
    {
        'game_id': 1,
        'players': ['player1', 'player2'],
        'p1': 'player1',
        'p2': 'player2',
        'f1': 5,
        's1': 6,
        'f2': 7,
        's2': 8,
        'f3': 9,
        's3': 10,
    },
    {
        'game_id': 2,
        'players': ['player1', 'player2'],
        'p1': 'player2',
        'p2': 'player1',
        'f1': 1,
        's1': 2,
        'f2': 3,
        's2': 4,
        'f3': 5,
        's3': 6,
    },
]
