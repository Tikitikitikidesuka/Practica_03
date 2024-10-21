from random import random, randint

from pycparser.ply.lex import NullLogger
from smartcard.System import readers

from arcade_card import ArcadeCard

TOKEN_COST = 1
TICKET_WIN = 5

def main():
    input("Insert card and press enter")

    connection = None

    try:
        reader = readers()[0]
        connection = reader.createConnection()
        connection.connect()
    except Exception as _:
        print("Could not read card")
        exit(1)

    card = ArcadeCard(connection, bytes([0xFF, 0xFF, 0xFF]))

    user_id, ok = card.read_id()
    print("Welcome " + user_id if ok else "GAMER")

    tokens, ok = card.read_tokens()
    if not ok or tokens < TOKEN_COST:
        print("Not enough tokens")
        exit(1)
    else:
        if not card.write_tokens(tokens - TOKEN_COST):
            print("Could not update tokens")
            exit(1)

    if randint(0, 1) == 0:
        print("You have won the game!!!")
        print("You get " + str(TICKET_WIN) + " tickets")
        tickets, ok_read = card.read_tickets()
        if not ok_read or not card.write_tickets(tickets + TICKET_WIN):
            print("Could not add tickets")
            print("Go to the counter for further help")
    else:
        print("You lose :(")


if __name__ == "__main__":
    main()