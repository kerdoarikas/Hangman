from Controller import Controller


class Hangman:

    def __init__(self):
        Controller().main()

if __name__ == '__main__':
    # DOTO read commandline db name
    Hangman()