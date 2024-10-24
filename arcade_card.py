import hmac
import hashlib

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

HMAC_ADDR = 0x40
HMAC_LENGTH = 0x10
HMAC_KEY = b'xX_GUTI33_Xx'


class ArcadeCard:
    def __init__(self, connection: CardConnection, psc: bytes):
        self.card = SLE5542(connection)
        self.card.select()
        self.card.present_psc(psc)

    def __update_hmac(self):
        id_data, _ = self.read_id()
        tickets, _ = self.read_tickets()
        tokens, _ = self.read_tokens()

        data = id_data.encode('ascii') + tickets.to_bytes(TICKETS_LENGTH, 'big') + tokens.to_bytes(TOKENS_LENGTH, 'big')

        hmac_value = hmac.new(HMAC_KEY, data, hashlib.md5).digest()

        success = self.card.write(HMAC_ADDR, HMAC_LENGTH, hmac_value)
        return success

    def write_id(self, id: str) -> bool:
        checked_id = id.encode('ascii')
        if len(checked_id) != ID_LENGTH:
            return False
        _, ok = self.card.write(ID_ADDR, ID_LENGTH, checked_id)
        if ok:
            self.__update_hmac()
        return ok

    def write_tickets(self, tickets: int) -> bool:
        _, ok = self.card.write(TICKETS_ADDR, TICKETS_LENGTH, tickets.to_bytes(TICKETS_LENGTH, 'big', signed=False))
        if ok:
            self.__update_hmac()
        return ok

    def write_tokens(self, tokens: int) -> bool:
        _, ok = self.card.write(TOKENS_ADDR, TOKENS_LENGTH, tokens.to_bytes(TOKENS_LENGTH, 'big', signed=False))
        if ok:
            self.__update_hmac()
        return ok

    def verify_hmac(self) -> bool:
        stored_hmac, _ = self.card.read(HMAC_ADDR, HMAC_LENGTH)

        id_data, _ = self.read_id()
        tickets, _ = self.read_tickets()
        tokens, _ = self.read_tokens()

        data = id_data.encode('ascii') + tickets.to_bytes(TICKETS_LENGTH, 'big') + tokens.to_bytes(TOKENS_LENGTH, 'big')

        calculated_hmac = hmac.new(HMAC_KEY, data, hashlib.md5).digest()

        return hmac.compare_digest(bytes(stored_hmac), calculated_hmac)

    def reset(self) -> bool:
        return self.write_id(ID_DEFAULT) and self.write_tickets(TICKETS_DEFAULT) and self.write_tokens(TOKENS_DEFAULT)

    def read_id(self) -> tuple[str, bool]:
        data, ok = self.card.read(ID_ADDR, ID_LENGTH)
        return toASCIIString(list(data)), ok

    def read_tickets(self) -> tuple[int, bool]:
        data, ok = self.card.read(TICKETS_ADDR, TICKETS_LENGTH)
        return int.from_bytes(data, 'big', signed=False), ok

    def read_tokens(self) -> tuple[int, bool]:
        data, ok = self.card.read(TOKENS_ADDR, TOKENS_LENGTH)
        return int.from_bytes(data, 'big', signed=False), ok