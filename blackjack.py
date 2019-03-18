'''
IMPLEMENTATION OF SIMPLIFIED BLACKJACK FOR COMPLETE PYTHON BOOTCAMP
AUTHOR: DANIEL CLEMES KÜLKAMP
'''

import random

class Card():
    '''
    Playing cards class (from A to 10, J Q and K )
    and suits of clubs, hears, spades and diamonds or joker
    '''
    SUITS = ['clubs', 'hearts', 'spades', 'diamonds']
    SYMBOLS = {'clubs': '♣', 'hearts': '♥', 'spades':'♠', 'diamonds':'♦'}
    FACE_VALUES = ['JOKER', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, value, suit):
        '''
        Constructor for Card,
        parameters:
        value: int from 0 (joker) to 13 (king)
        suit: string in Cards.SUITS
        '''
        if not isinstance(value, int):
            raise TypeError("must be in int")
        if value < 0 or value > 13:
            raise ValueError("must be in >=0 and <=13")
        if not isinstance(suit, str):
            raise TypeError("must be in string")
        if suit not in Card.SUITS and value != 0:
            raise ValueError("must be in Cards.SUITS list")

        self.value = value
        self.suit = suit

    def long_description(self):
        '''
        returns the long description of the card
        example: card.long_description()
        ==> 'The Ace of Spades'
        '''
        long_values = ['JOKER', 'Ace', 'Two', 'Three', 'Four', 'Five', 'Six',\
        'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
        if self.value > 0:
            return 'The '+ long_values[self.value] + ' of ' + self.suit.capitalize()
        return 'The Joker'


    def __str__(self):
        '''
        returns a short description of the card in the form value suit
        examples: A♣, 10♠, Q♥, J♦, 4♠, joker
        '''
        if self.value == 0:
            return 'JOKER'
        return Card.FACE_VALUES[self.value]+Card.SYMBOLS[self.suit]

class Deck():
    '''
    standard playing cards deck of 52 cards

    '''

    def __init__(self, empty=False, jokers=0):
        '''
        default constructor
        '''
        self.cards = []
        if empty:
            return
        for suit in ['clubs', 'hearts', 'spades', 'diamonds']:
            for value in range(1, 14):
                self.cards.append(Card(value, suit))
        for _ in range(0, jokers):
            self.cards.append(Card(0, ''))


    def shuffle(self):
        '''
        shuffles the deck  sort receives a key function with one argument
        '''
        self.cards.sort(key=lambda x: random.uniform(0, 1))

    def draw_card(self):
        '''
        pops the first element of the deck and returns it
        '''
        if self.cards == []:
            raise ValueError("drawing from empty deck")
        return self.cards.pop(0)

    def __str__(self):
        '''
        returns a string with the cards in the form '[A♣, 10♠, Q♥, J♦, 4♠]'
        '''
        description = '['
        for card in self.cards:
            description += str(card)+', '
        description = description[:-2]+"]" #replaces the last ', ' with ']'
        return description

class BlackJackHand(Deck):
    '''
    Defines a hand of cards. subclass of deck for convenience
    '''

    def __init__(self):
        '''
        Default constructor, creates an empty hand
        '''
        Deck.__init__(self, empty=True)
        self.total = 0
        self.soft = False

    def add(self, card):
        '''
        adds a card to the hand, updates the total and soft
        returns new total value of hand
        '''
        self.cards.append(card)
        if card.value == 1: #if card is an ace
            if self.total <= 10:
                self.soft = True
                self.total += 11
            else:
                self.total += 1
        else:
            increment = 0
            if card.value > 10: #jack, queen and king are worth 10
                increment = 10
            else:
                increment = card.value
            self.total += increment
        if self.total > 21 and self.soft:
            self.total -= 10
            self.soft = False
        return self.total

    def show(self):
        '''
        prints the cards in the hand and the total value
        ex: "A♣, 10♠ - Total: 21
        '''
        hand_text = ""
        for card in self.cards:
            hand_text += str(card)
        hand_text += f' - Total: {self.total}'
        return hand_text

    def __str__(self):
        '''
        wraper for show(self)
        '''
        return "["+self.show()+"]"

class Player():
    '''
    Black jack player.
    Has a balance and a Hand
    '''
    def __init__(self, balance=100, deck=None):
        '''
        constructor for player.
        Initializes balance and Hand with first two cards
        parameters:
            balance -> inicial balance
            deck -> deck from which cards are drawn
        '''
        self.balance = balance
        self.hand = BlackJackHand()
        if deck:
            self.draw_two(deck)
        print(f'Player initialized with balance: {self.balance} and hand {self.hand}')


    def draw_two(self, deck):
        '''
        draws the first two cards of a blackjack game.
        upddates hand

        '''
        self.hand.add(deck.draw_card())
        self.hand.add(deck.draw_card())


    def place_bet(self, value):
        '''
        Places a bet using player's balance.
        Parameters:
            value -> number
        If value bigger than balance, raises ValueError
        '''
        if value <= self.balance:
            self.balance -= value
            return value
        raise ValueError('Not enough funds')

    def hit_me(self, deck):
        '''
        draws a card from a deck and updates hand
        parameters: deck -> deck from which player draws a card
        '''
        self.hand.add(deck.draw_card())

class Dealer(Player):
    '''
    Black Jack dealer
    '''
    def __init__(self, deck):
        '''
        Constructor for blackjack dealer.
        parameters: 
            deck
        '''
        self.hand = BlackJackHand()
        self.hand.add(deck.draw_card())
        print(f'Dealers Hand: {self.hand}')


class BlackJackGame():
    '''
    Main class for Blackjack game
    '''
    def __init__(self):
        '''
        creates the game objects
        '''
        self.deck = Deck(jokers=0)
        self.deck.shuffle()
        #prints instructions:
        print('Welcome to blackjack!')
        self.player = None
        while not self.player:
            try:
                bal = int(input('Enter your initial amount of coins: '))
                self.player = Player(bal, self.deck)
            except:
                pass
        self.dealer = Dealer(self.deck)

if __name__ == '__main__':
    game = BlackJackGame()

        