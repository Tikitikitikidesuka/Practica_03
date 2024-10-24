from smartcard.System import readers

from arcade_card import ArcadeCard

if __name__ == '__main__':
    card = None

    try:
        reader = readers()[0]
        connection = reader.createConnection()
        connection.connect()
    except Exception as _:
        print("Could not connect to card")
        exit(1)

    card = ArcadeCard(connection, bytes([0xFF, 0xFF, 0xFF]))

    option = ""
    while option != "e":
        option = ""
        while option not in ["a", "b", "c", "d", "e"]:
            print("\nPick an option:")
            print(" a) Create card")
            print(" b) Set tokens")
            print(" c) Set tickets")
            print(" d) Show card info")
            print(" e) Exit")
            option = input("Your option: ")
            print()

        if option == "a":
            ok = card.reset()
            if not ok:
                print("Error reseting card")
                continue
            id_str = input("Card ID (16 chars): ").ljust(16)
            if len(id_str) > 16:
                print("ID must be shorter than 16 chars")
                continue

            ok = card.write_id(id_str)
            if not ok:
                print("Invalid ID")
                continue

        elif option == "b":
            ok = card.write_tokens(int(input("Tokens: ")))
            if not ok:
                print("Could not write tokens")
                continue

        elif option == "c":
            ok = card.write_tickets(int(input("Tickets: ")))
            if not ok:
                print("Could not write tickets")
                continue

        elif option == "d":
            id_data, id_ok = card.read_id()
            token_data, token_ok = card.read_tokens()
            ticket_data, ticket_ok = card.read_tickets()

            if not id_ok or not token_ok or not ticket_ok:
                print("Could not read data")
                continue

            print("ID: " + id_data)
            print("TOKENS: " + str(token_data))
            print("TICKETS: " + str(ticket_data))
