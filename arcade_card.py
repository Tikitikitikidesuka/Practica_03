from smartcard.CardConnection import CardConnection
from smartcard.util import toASCIIString

from sle5542 import SLE5542

ID_ADDR = 0x20
ID_LENGTH = 0x10
ID_DEFAULT = "0" * 16

TICKETS_ADDR = 0x30
TICKETS_LENGTH = 0x04
TICKETS_DEFAULT = 0

TOKENS_ADDR = 0x34
TOKENS_LENGTH = 0x04
TOKENS_DEFAULT = 0


class ArcadeCard:
    def __init__(self, connection: CardConnection, psc: bytes):
        self.card = SLE5542(connection)
        self.card.select()
        self.card.present_psc(psc)

    def reset(self) -> bool:
        return self.write_id(ID_DEFAULT) and self.write_tickets(TICKETS_DEFAULT) and self.write_tokens(TOKENS_DEFAULT)

    def read_id(self) -> tuple[str, bool]:
        data, ok = self.card.read(ID_ADDR, ID_LENGTH)
        return toASCIIString(list(data)), ok

    def write_id(self, id: str) -> bool:
        checked_id = id.encode('ascii')
        if len(checked_id) != ID_LENGTH: return False
        _, ok = self.card.write(ID_ADDR, ID_LENGTH, checked_id)
        return ok

    def read_tickets(self) -> tuple[int, bool]:
        data, ok = self.card.read(TICKETS_ADDR, TICKETS_LENGTH)
        return int.from_bytes(data, 'big', signed=False), ok

    def read_tokens(self) -> tuple[int, bool]:
        data, ok = self.card.read(TOKENS_ADDR, TOKENS_LENGTH)
        return int.from_bytes(data, 'big', signed=False), ok

    def write_tickets(self, tickets: int) -> bool:
        _, ok = self.card.write(TICKETS_ADDR, TICKETS_LENGTH, tickets.to_bytes(TICKETS_LENGTH, 'big', signed=False))
        return ok

    def write_tokens(self, tokens: int) -> bool:
        _, ok = self.card.write(TOKENS_ADDR, TOKENS_LENGTH, tokens.to_bytes(TOKENS_LENGTH, 'big', signed=False))
        return ok
