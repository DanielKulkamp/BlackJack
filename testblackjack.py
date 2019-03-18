import unittest
import blackjack

class TestBlackJack(unittest.TestCase):
    '''
    Tests the game BlackJack.py
    '''

    def test_create_valid_cards(self):
        '''
        creates all valid cards and test the creation
        '''
        for value in range(14):
            for suit in ['clubs', 'hearts', 'spades', 'diamonds']:
                card = blackjack.Card(value,suit)
                self.assertIsInstance(card, blackjack.Card)

    def test_create_invalid_card_value(self):
        '''
        tests exception 
        '''
        self.assertRaises(ValueError, blackjack.Card, 14, 'clubs')

    def test_string_value(self):
        self.assertEqual('A♣', str(blackjack.Card(1,'clubs')))

    def test_create_deck_with_joker(self):
        deck = blackjack.Deck(jokers=1)
        self.assertEqual(53, len(deck.cards))
        
    def test_create_deck_without_joker(self):
        deck = blackjack.Deck(jokers=0)
        self.assertEqual(52, len(deck.cards))

    def test_shuffle_deck(self):
        deck = blackjack.Deck(jokers=1)
        desc = str(deck)
        self.assertNotEqual(desc, str(deck.shuffle()))
    
    def test_create_empty_deck(self):
        deck = blackjack.Deck(empty=True)
        self.assertEqual([],deck.cards)

    def test_hand(self):
        hand = blackjack.BlackJackHand()
        self.assertEqual(hand.total,0)
        hand.add(blackjack.Card(1,'spades'))
        self.assertEqual(hand.total,11)
        hand.add(blackjack.Card(11,'spades'))
        self.assertEqual(hand.total,21)
        hand.add(blackjack.Card(13,'spades'))
        self.assertEqual(hand.total,21)

    def test_player_cration(self):
        deck = blackjack.Deck(jokers=0)
        player = blackjack.Player(100,deck)
        self.assertEqual(len(player.hand.cards),2)

    def test_place_valid_bet(self):
        deck = blackjack.Deck(jokers=0)
        player = blackjack.Player(100,deck)
        player.place_bet(12)
        self.assertEqual(88,player.balance)

    def test_place_invalid_bet(self):
        deck = blackjack.Deck(jokers=0)
        player = blackjack.Player(100,deck)
        self.assertRaises(ValueError, player.place_bet, 120)        

    def test_unique_deck(self):
        deck = blackjack.Deck(jokers=0)
        print(deck)
        player = blackjack.Player(100, deck)
        print(player.hand)
        print(deck)
        self.assertEqual(len(deck.cards),50)



if __name__ == '__main__':
    def spam(eggs):
        eggs.append(1)
        eggs = [2, 3]

    ham = [0]
    spam(ham)
    print(ham)

    unittest.main()