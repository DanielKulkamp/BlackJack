# -*- coding: UTF-8 -*-
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
        hand_text = "[ " 
        if len(self.cards) > 0:
            hand_text += str(self.cards[0])
        if len(self.cards) > 1:
            for card in self.cards[1:]:
                hand_text += ", " +str(card)
        hand_text += f' ] - Total: {self.total}'
        return hand_text

    def __str__(self):
        '''
        wraper for show(self)
        '''
        return "["+self.show()+"]"

class BasePlayer():
    '''
    Base class for blackjack player
    '''
    def __init__(self):
        '''
        Base constructor. Initializes an empty hand
        '''
        self.hand = BlackJackHand()

    def hit_me(self, deck):
        '''
        draws a card from a deck and updates hand
        parameters: deck -> deck from which player draws a card
        '''
        self.hand.add(deck.draw_card())

    def show_status(self):
        '''
        subclasses must implement...

        '''
        print(f'Hand: {self.hand.show()}')

    def clear_hand(self):
        '''
        clears by setting self.hand to a new empty blackjackhand
        '''
        self.hand = BlackJackHand()

class HumanPlayer(BasePlayer):
    '''
    Black jack player.
    Has a balance and a Hand
    '''
    def __init__(self, balance=100):
        '''
        constructor for player.
        Initializes balance and Hand with first two cards
        parameters:
            balance -> inicial balance
            deck -> deck from which cards are drawn
        '''
        BasePlayer.__init__(self)
        self.balance = balance
        print(f'Human Player Initialized with hand {self.hand} and balance {self.balance}')

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


class Dealer(BasePlayer):
    '''
    Black Jack dealer
    '''
    def __init__(self):
        '''
        Constructor for blackjack dealer.
        parameters:
            none
        '''
        BasePlayer.__init__(self)
        print(f'Dealer initialized!')

    def show_status(self):
        '''
        Prints dealer hand.
        '''
        print('Dealer ', end="")
        BasePlayer.show_status(self)

class BlackJackGame():
    '''
    Main class for Blackjack game
    '''
    def __init__(self):
        '''
        creates the game objects and prints initial instructions
        '''
        #prints instructions:
        print('Welcome to blackjack!')
        self.player = None
        self.deck = None
        self.current_bet = 0
        while not self.player:
            try:
                bal = int(input('Enter your initial amount of coins: '))
                self.player = HumanPlayer(bal)
            except ValueError as exception:
                print(exception)
        self.dealer = Dealer()

    def human_win(self):
        '''Pays rewards for winning. ask for another round'''
        self.player.balance += 2*self.current_bet
        print(f'You won that one!\nYour current balance is {self.player.balance}')


    def human_lose(self):
        '''Updates balance.'''
        print(f'You lost that one!\nYour current balance is {self.player.balance}')


    def get_another_one(self):
        '''ask for another round. if so, play it'''
        selected = ''
        while selected not in ['y', 'n']:
            try:
                selected = input('Wanna play another one? (y/n): ')
            except ValueError as error:
                print(f"Value Error {error}")
                self.get_another_one()
        return selected == 'y'


    def play_round(self):
        '''Plays one round of blackjack'''
        self.deck = Deck(jokers=0)
        self.deck.shuffle()
        self.dealer.clear_hand()
        self.player.clear_hand()
        self.dealer.hit_me(self.deck)
        self.dealer.show_status()
        self.player.draw_two(self.deck)
        self.player.show_status()
        self.set_current_bet()
        self.player_turn()
        if self.player.hand.total == 21:
            self.human_win()
            return
        if self.player.hand.total > 21:
            self.human_lose()
            return
        self.dealer_turn()


    def set_current_bet(self):
        '''
        Ask player to input the current bet
        '''
        try:
            self.current_bet = self.player.place_bet(int(input('Enter your bet: ')))
        except ValueError:
            print("Either you entered a wrong value or you don't have that much...")
            self.set_current_bet()
            return

    def player_turn(self):
        '''
        Show current hand and asks for 'hit me ('h' or
        '''
        while True:
            try:
                action = input('Hit me (h) or stop (s): ')
                
            except ValueError as exception:
                print(exception)
            finally: 
                if action not in ['h', 's']:
                    continue
            if action == 'h':
                self.player.hit_me(self.deck)
                self.player.show_status()
                if self.player.hand.total >= 21:
                    return
            else:
                return


    def dealer_turn(self):
        '''
        Dealer Turn. Draws cards until win or bust.
        '''
        print("Now it is the dealer turn")
        while self.dealer.hand.total < self.player.hand.total:
            self.dealer.hit_me(self.deck)
            self.dealer.show_status()
        if self.dealer.hand.total <= 21:
            self.human_lose()
        else:
            self.human_win()

if __name__ == '__main__':

    GAME = BlackJackGame()
    while True:
        GAME.play_round()
        if GAME.player.balance < 1:
            print("Guards take this worthless beggar out of my casino!")
            break
        if not GAME.get_another_one():
            print("Good bye, then!")
            break
        print("Lets go!")
