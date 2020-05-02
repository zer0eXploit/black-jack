'''
A simple black jack game
'''

import random

suits = (
    'Hearts', 'Diamonds', 'Spades', 'Clubs'
)
ranks = (
    'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
    'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace',
)

values = {
    'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5,
    'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9,
    'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10,
    'Ace': 11
}

PLAYING = True


class Card:
    '''
    A card class
    '''

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def surpress_warning(self):
        '''
        Just an empty function to surpress pylint warning
        '''

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck():
    '''
    A deck of cards class
    '''

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        return f'{self.deck}'

    def shuffle(self):
        '''
        Shuffles the deck of cards
        '''
        random.shuffle(self.deck)

    def deal(self):
        '''
        Deals a card to the player
        '''
        return self.deck.pop()


class Hand:
    '''
    A hand class to calculate sums of cards
    '''

    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
        self.ace_sum = 0

    def adjust_for_ace(self):
        '''
        Adjusts the ace value appropiately
        '''
        self.value -= self.ace_sum
        self.ace_sum = 0
        for _ in range(0, self.aces):
            if self.value + 10 > 21:
                self.value += 1
                self.ace_sum += 1
            else:
                self.value += 10
                self.ace_sum += 10

    def add_card(self, card):
        '''
        Sums the value of cards
        '''
        self.cards.append(card)
        if card.rank == "Ace":
            self.aces += 1
        else:
            self.value += values[card.rank]
        self.adjust_for_ace()


class Chips:
    '''
    User balance management class
    '''

    def __init__(self, bet=0):
        self.total = 100  # 100 as initial value
        self.bet = bet

    def win_bet(self):
        '''
        Add winning bet to total
        '''
        self.total += self.bet

    def lose_bet(self):
        '''
        Deduce loosing amount from total
        '''
        self.total -= self.bet


def take_bet(chips):
    '''
    Asks user of their desired bet
    '''

    while True:
        print(f'Initial chips: {chips.total}')
        try:
            bet_amt = int(input("Please enter amount to bet: "))
            if bet_amt > chips.total or bet_amt == 0:
                print("Insufficient funds!")
                continue
            chips.bet = bet_amt
            print("I am betting {0}.".format(chips.bet))
        except ValueError:
            print("Invalid amount!")
            continue
        except TypeError:
            print("Invalid amount!")
            continue
        else:
            break


def hit(deck, hand):
    '''
    Draws a card from the deck and adds card values
    '''
    card = deck.deal()  # deal a card off from deck
    hand.add_card(card)  # add the card to hand


def hit_or_stand(deck, hand):
    '''
    Asks the user to hit or statnd
    '''
    global PLAYING  # to control an upcoming while loop

    hit_not = input("Hit? [Y]es or [N]o?: ")
    if hit_not in ("Y", "y"):
        hit(deck, hand)
    else:
        PLAYING = False


def show_some(player, dealer):
    '''
    Shows some of dealer cards and all of player's
    '''

    print("")
    print("Dealer Cards.")
    print("< -- CARD HIDDEN -- >")
    print(dealer.cards[-1], end="\n\n")
    print("Player Cards.")
    print(*player.cards, sep="\n")
    print("")


def show_all(player, dealer):
    '''
    Shows all of the cards of the players
    '''
    print("")
    print("Dealer Cards.")
    print(*dealer.cards, sep="\n", end="\n\n")
    print("Player Cards.")
    print(*player.cards, sep="\n")
    print("")


def player_wins(chips):
    '''
    Function to call when player wins
    '''
    print("PLAYER WINS!")
    chips.win_bet()


def dealer_wins(chips):
    '''
    Function to call when dealer wins
    '''

    print("DEALER WINS!")
    chips.lose_bet()


def push():
    '''
    Function to call when the game is a tie
    '''

    print("Dealer and Player tie! It's a push.")


def ask_play_again():
    '''
    Asks the play if they want to continue
    '''
    global PLAYING

    if input("Play again? Y[es] or press any to exit: ") in ('y', 'Y'):
        PLAYING = True
        return True

    PLAYING = False
    return False


player_chips = Chips()  # Set up the Player's chips
print("Welcome to simple black jack game!")

while True:

    card_deck = Deck()
    card_deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(card_deck.deal())
    player_hand.add_card(card_deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(card_deck.deal())
    dealer_hand.add_card(card_deck.deal())

    take_bet(player_chips)  # Prompt the Player for their bet

    show_some(player_hand, dealer_hand)

    while PLAYING:  # if the player still wants to play

        hit_or_stand(card_deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            print(f'Player busted! Total: {player_hand.value}')
            show_some(player_hand, dealer_hand)
            break

    # dealer only hits if the player is not busted
    if player_hand.value < 21:
        while dealer_hand.value < 17:
            dealer_hand.add_card(card_deck.deal())

        if dealer_hand.value > 21:
            print(f'Dealer burst! Total: {dealer_hand.value}')

    show_all(player_hand, dealer_hand)
    print(f'Player: {player_hand.value}')
    print(f'Dealer: {dealer_hand.value}', end='\n\n')

    # Run different winning scenarios
    if player_hand.value > 21:
        dealer_wins(player_chips)
    elif dealer_hand.value > 21:
        player_wins(player_chips)
    elif player_hand.value == dealer_hand.value:
        push()
    elif player_hand.value > dealer_hand.value:
        player_wins(player_chips)
    else:
        dealer_wins(player_chips)

    # Inform Player of their chips total
    print(f'Chips remaining: {player_chips.total}')

    # Ask to play again
    if player_chips.total > 0:
        if ask_play_again():
            continue
        break
    break
