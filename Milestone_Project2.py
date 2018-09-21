'''
Blackjack Game
By Isaiah Frey
Allows the user to play a one-on-one blackjack game vs. a dealer
The player will place bets on their initial hand and then hit or stay
The dealer will then hit until it beats the player or busts
Finally the player will recieve compensation for his bets
'''

#-----------------Libraries------------------------#
import random
import time

#------------------Classes-------------------------#

class Card:

	def __init__(self, rank, value, suit):
		self.rank = rank
		self.value = value
		self.suit = suit

	def __str__(self):
		return f"{self.rank} of {self.suit}"

class Deck:

	def __init__(self):
		'''
		Initialize the deck to contain 52 different cards
		'''
		self.deck = []
		for rank in RANK:
			for suit in SUIT:
				self.deck.append(Card(rank, VALUE[rank], suit))

	def __str__(self):

		deck_str = ""
		for card in self.deck:
			deck_str += '\n' + card.__str__()
		return deck_str

	def shuffle(self):
		'''
		Shuffle the deck 
		'''
		random.shuffle(self.deck)

	def deal(self):
		'''
		Deal a single card
		'''
		return self.deck.pop()

class Hand:

	def __init__(self):
		self.cards = []
		self.aces = 0
		self.total = 0

	def find_total(self):
		for card in self.cards:
			self.total += card.value
		while self.total > 21 and self.aces > 0:
			self.total -= 10
			self.aces -= 1
		return self.total

	def __str__(self):

		hand_str = ""
		for card in self.cards:
			hand_str += '\n' + card.__str__()
		return hand_str

class Money:

	def __init__(self):
		self.money = 1000

	def bet(self, bet):
		print(f"You placed a bet for ${bet}.")
		self.money -= bet
		print(f"You have ${self.money} left.\n")






#---------------Global Variables--------------------#

RANK = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
VALUE = {'Ace': 11, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10}
SUIT = ['Spades', 'Clubs', 'Diamonds', 'Hearts']

#----------------Main-------------------------------#

account = Money()
print("Welcome to Blackjack!")

#Game loop
while True:

	#Print a few empty lines to seperate games
	print("\n\n\n")

	#Initialize the player's and dealer's hands and player's account
	player_hand = Hand()
	dealer_hand = Hand()
	bust = False

	#To begin the game, make a deck and shuffle it
	deck = Deck()
	deck.shuffle()

	#Ask the player for a bet
	while True:
		try:
			bet = int(input("Please place a bet: "))
		except ValueError:
			print("Please input a value")
			continue
		if bet > account.money:
			print(f"You don't have ${bet}! You have ${account.money} remaining.")
			continue
		else:
			account.bet(bet)
			break

	#Deal the player two cards
	for i in range(2):
		player_hand.cards.append(deck.deal())
	print(f"Your hand is: {player_hand}\n")

	#Deal two cards to the dealer, showing the player the first one
	dealer_hand.cards.append(deck.deal())
	print(f"The dealer's face up card is: {dealer_hand}\n")
	dealer_hand.cards.append(deck.deal())

	#Ask the player if they would like another card
	while True:

		hit = input("Would you like another card? Enter y for yes or n for no: ")

		if hit.lower() == 'y':
			player_hand.cards.append(deck.deal())
			print(f"\nYour hand is: {player_hand}")
			#Count the number of aces in the hand
			player_hand.aces = 0

			#Add up the aces in the player's hand
			for card in player_hand.cards:
				if card.rank == 'Ace':
					player_hand.aces += 1

			#Check for bust
			if player_hand.find_total() > 21:
				print("You busted!")
				bust = True
				break
		else:
			break

	#If the player busted, end the round
	if bust:
		play_again = input("Would you like to play again? Enter a y for yes or n for no: ")
		if play_again.lower() == 'y':
			continue
		else:
			break

	#Otherwise give the dealer a chance to beat the player
	print()
	print("Dealer's turn.")
	print(f"The dealer's hand is {dealer_hand}")
	player_total = player_hand.find_total()

	while (dealer_hand.find_total() < player_total or dealer_hand.find_total() < 17) and not bust:

		#Wait for a short while before playing to give the player a chance to see what's happening
		time.sleep(2)

		#Print a blank line
		print()

		#Deal the dealer a card
		dealer_hand.cards.append(deck.deal())
		print(f"The dealer's hand is {dealer_hand}")

		#Add up the aces
		for card in dealer_hand.cards:
			if card.rank == 'Ace':
				dealer_hand.aces += 1

		#Check for busts
		if dealer_hand.find_total() > 21:
			print("Dealer busted!\n")
			bust = True
			break

	#If the computer bust double the player's bet
	if bust:
		print(f"Congratulations you won ${bet*2}!")
		account.money += bet*2
		print(f"You now have ${account.money} in your account.")

	#Otherwise the computer won
	else:
		print(f"The dealer won. You now have ${account.money} in your account.")

	#Ask the player if they would like to play again
	play_again = input("Would you like to play again? Enter a y for yes or n for no: ")
	if play_again.lower() == 'y':
		continue
	else:
		break
		