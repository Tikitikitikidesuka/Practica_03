print("El print te sobra");

card = new Card();
atr = card.reset(Card.RESET_COLD);

print(atr);
print("ok");

card.plainApdu(new ByteString("FF A4 00 00 01 06", HEX));


function resetCard(card) {
	// Reset card to zero
}

function writeUser(card, user_id) {
	// Write user ID to card
}

function readUser(card) {
	
}

function writeTokens(card, tokens) {
	
}

function readTokens(card) {
	
}

function writeTickets(card, tickets) {
	
}

function readTickets(card) {
	
}

