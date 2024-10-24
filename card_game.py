from random import randint

from smartcard.System import readers

from arcade_card import ArcadeCard

TOKEN_COST = 1
TICKET_WIN = 5

def main():
    while True:
        input("Insert card and press enter")

        connection = None

        try:
            reader = readers()[0]
            connection = reader.createConnection()
            connection.connect()
        except Exception as _:
            print("Could not read card")
            continue

        card = ArcadeCard(connection, bytes([0xFF, 0xFF, 0xFF]))

        if not card.verify_hmac():
            print("The card has been tampered with >:(")
            connection.disconnect()
            continue

        user_id, ok = card.read_id()
        print("Welcome " + user_id if ok else "GAMER")

        tokens, ok = card.read_tokens()
        if not ok or tokens < TOKEN_COST:
            print("Not enough tokens")
            connection.disconnect()
            continue
        else:
            if not card.write_tokens(tokens - TOKEN_COST):
                print("Could not update tokens")
                connection.disconnect()
                continue

        if randint(0, 1) == 0:
            print("You have won the game!!!")
            print("You get " + str(TICKET_WIN) + " tickets")
            tickets, ok_read = card.read_tickets()
            if not ok_read or not card.write_tickets(tickets + TICKET_WIN):
                print("Could not add tickets")
                print("Go to the counter for further help")
        else:
            print("You lose :(")

        connection.disconnect()


if __name__ == "__main__":
    main()