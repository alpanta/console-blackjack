import random

suits = ('Hearts', 'Spades', 'Diamonds', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen',
         'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9,
          'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
playing = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return str(self.rank) + ' of ' + str(self.suit)


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()
        return 'The deck is ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    value: int

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self):
        self.total_chips = 100
        self.bet = 0

    def win_bet(self):
        self.total_chips += self.bet

    def lose_bet(self):
        self.total_chips -= self.bet


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Invalid bet.')
        else:
            if chips.bet > chips.total_chips:
                print('Sorry, you do not have enough chips.')
            else:
                break


def hit_or_stand(deck, hand):
    global playing

    while True:
        call = input("Would you like to Hit or Stand? (H/S): ")
        if call.lower() == 'h':
            hit(deck, hand)
        elif call.lower() == 's':
            print('You stand. Dealer plays.')
            playing = False
        else:
            print('Invalid call.')
            continue
        break


def show_early(player, dealer):
    print("\nDealer's Hand:")
    print("?")
    print(dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n')


def show_winner(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n')
    print("\nDealer's Hand is ", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n')
    print("\nPlayer's Hand is ", player.value)


def player_busts(player, dealer, chips):
    print("\nPlayer busts!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("\nPlayer wins!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("\nDealer busts!")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("\nDealer wins!")
    chips.lose_bet()


def push(player, dealer):
    print("Player and Dealer tie. It is a push!")


if __name__ == '__main__':
    while True:
        print("Welcome to Dealer's Game!")
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        player_chips = Chips()
        take_bet(player_chips)

        show_early(player_hand, dealer_hand)

        while playing:
            hit_or_stand(deck, player_hand)
            show_early(player_hand, dealer_hand)
            if player_hand.value > 21:
                player_busts(player_hand, dealer_hand, player_chips)
                break
        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)
            show_winner(player_hand, dealer_hand)
            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)
            else:
                push(player_hand, dealer_hand)
        print("Player's balance is {}".format(player_chips.total_chips))
        new_game = input("Would you like to play more cards? (Y/N): ")

        if new_game.lower() == 'y':
            playing = True
            continue
        elif new_game.lower() == 'n':
            break