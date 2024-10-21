from smartcard.CardConnection import CardConnection


class SLE5542:
    def __init__(self, card_connection: CardConnection):
        """
        Initializes the SLE5542 instance with a given card connection.

        Args:
            card_connection (CardConnection): The connection to the smart card.
        """
        self.card_connection = card_connection

    @staticmethod
    def __format_return(card_return: tuple[any, any, any]) -> tuple[bytes, bool]:
        """
        Private method: Formats the card interface output into (data, ok) format.

        Args:
            card_return (tuple[any, any, any]): A tuple containing data and status codes.

        Returns:
            tuple[bytes, bool]: A tuple containing the data as bytes and a boolean indicating success.
        """
        return card_return[0], (card_return[1] == 0x90 and card_return[2] == 0x00)

    def __transmit_command(self, command: bytes) -> tuple[bytes, bool]:
        """
        Private method: Transmits a command to the card and formats the response.

        Args:
            command (bytes): The command to transmit to the card.

        Returns:
            tuple[bytes, bool]: A tuple containing the response data and a boolean indicating success.
        """
        return SLE5542.__format_return(self.card_connection.transmit(list(command)))

    def select(self) -> tuple[bytes, bool]:
        """
        Selects the card for communication.

        Returns:
            tuple[bytes, bool]: A tuple containing the response data and a boolean indicating success.
        """
        command = [0xFF, 0xA4, 0x00, 0x00, 0x01, 0x06]
        return self.__transmit_command(bytes(command))

    def read_psc_error_counter(self) -> tuple[bytes, bool]:
        """
        Reads the PSC error counter from the card.

        Returns:
            tuple[bytes, bool]: A tuple containing the PSC error counter data and a boolean indicating success.
        """
        command = [0xFF, 0xB1, 0x00, 0x00, 0x04]
        return self.__transmit_command(bytes(command))

    def present_psc(self, psc: bytes) -> tuple[bytes, bool]:
        """
        Presents the PSC (Personal Security Code) to the card.

        Args:
            psc (bytes): The 3-byte PSC to be presented.

        Returns:
            tuple[bytes, bool]: A tuple containing the response data and a boolean indicating success.

        Raises:
            ValueError: If the PSC is not exactly 3 bytes or contains invalid values.
        """
        if len(psc) != 3 or not all(0x00 <= x <= 0xFF for x in psc):
            raise ValueError("Invalid psc")

        command = [0xFF, 0x20, 0x00, 0x00, 0x03] + list(psc)
        return self.__transmit_command(bytes(command))

    def change_psc(self, psc: bytes) -> tuple[bytes, bool]:
        """
        Changes the PSC (Personal Security Code) on the card.

        Args:
            psc (bytes): The new 3-byte PSC to be set.

        Returns:
            tuple[bytes, bool]: A tuple containing the response data and a boolean indicating success.

        Raises:
            ValueError: If the PSC is not exactly 3 bytes or contains invalid values.
        """
        if len(psc) != 3 or not all(0x00 <= x <= 0xFF for x in psc):
            raise ValueError("Invalid psc")

        command = [0xFF, 0xD2, 0x00, 0x01, 0x03] + list(psc)
        return self.__transmit_command(bytes(command))

    def read(self, address: int, length: int) -> tuple[bytes, bool]:
        """
        Reads data from the card at a specified address and length.

        Args:
            address (int): The address from which to start reading (0x00 to 0xFF).
            length (int): The number of bytes to read (1 to 255).

        Returns:
            tuple[bytes, bool]: A tuple containing the read data and a boolean indicating success.

        Raises:
            ValueError: If the address or length is out of valid range.
        """
        if address < 0x00 or address >= 0x100:
            raise ValueError("Invalid address")
        if length <= 0x00 or length >= 0x100:
            raise ValueError("Invalid length")

        command = [0xFF, 0xB0, 0x00, address, length]
        return self.__transmit_command(bytes(command))

    def write(self, address: int, length: int, data: bytes) -> tuple[bytes, bool]:
        """
        Writes data to the card at a specified address and length.

        Args:
            address (int): The address at which to start writing (0x00 to 0xFF).
            length (int): The number of bytes to write (1 to 255).
            data (bytes): The data to be written.

        Returns:
            tuple[bytes, bool]: A tuple containing the response data and a boolean indicating success.

        Raises:
            ValueError: If the address, length, or data size is invalid.
        """
        if address < 0x00 or address >= 0x100:
            raise ValueError("Invalid address")
        if length <= 0x00 or length >= 0x100:
            raise ValueError("Invalid length")
        if len(data) != length:
            raise ValueError("Data length mismatch")

        command = [0xFF, 0xD0, 0x00, address, length] + list(data)
        return self.__transmit_command(bytes(command))

    def write_protect(self, address: int, length: int, data: bytes) -> tuple[bytes, bool]:
        """
        Applies write protection to a section of memory on the card.

        Args:
            address (int): The address at which to start write protection (0x00 to 0x1F).
            length (int): The number of bytes to protect (1 to 32).
            data (bytes): The data to write protect.

        Returns:
            tuple[bytes, bool]: A tuple containing the response data and a boolean indicating success.

        Raises:
            ValueError: If the address, length, or data size is invalid.
        """
        if address < 0x00 or address >= 0x20:
            raise ValueError("Invalid address")
        if length <= 0x00 or length > 0x20:
            raise ValueError("Invalid length")
        if len(data) != length:
            raise ValueError("Data length mismatch")

        command = [0xFF, 0xD1, 0x00, address, length] + list(data)
        return self.__transmit_command(bytes(command))
