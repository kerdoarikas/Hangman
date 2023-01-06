import glob


class Model:

    def __init__(self):
        self.database_name = 'databases/hangman_words_ee.db'
        self.image_files = glob.glob('images/*.png')  # All hangman images
        # New Game
        self.new_word = None  # random word from db
        self.user_word = []  # empty list
        self.all_user_chars = []  # Any letters entered incorrectly
        self.counter = 0  # Error counter (wrong letters)
        # Leaderboard
        self.player_name = 'UNKNOWN'
        self.leaderboard_file = 'leaderboard.txt'
        self.score_data = []  # Leaderboard file content
