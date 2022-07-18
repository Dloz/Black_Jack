import random
import time


def clear_function():
    print('\n' * 100)


suits = ('Hearts', 'Spades', 'Diamonds', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2,
          'Three': 3,
          'Four': 4,
          'Five': 5,
          'Six': 6,
          'Seven': 7,
          'Eight': 8,
          'Nine': 9,
          'Ten': 10,
          'Jack': 10,
          'Queen': 10,
          'King': 10,
          'Ace': 11}


class CardClass:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class DeckClass:

    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(CardClass(suit, rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()


class PlayerClass:

    def __init__(self, name, bank=1000000):
        self.name = name
        self.bank = bank
        self.hand = []
        self.score = 0

    def clean(self):
        self.hand = []
        self.score = 0

    def get(self, card):
        self.hand.append(card)
        self.score += card.value

        if self.score > 21:
            for card in self.hand:
                if card.rank == 'Ace':
                    card.rank = 'Ace*'
                    self.score -= 10

    def money_transfer(self, amount):
        self.bank += amount

    def bet(self):
        # informing about bank status
        print(f"{self.name}, you current bank is {self.bank}\n")
        while True:
            try:
                amount = int(input("Provide amount of the bet: "))

                if amount <= 0:
                    print("Please, provide positive number")
                    continue

                elif amount <= self.bank:
                    print("Bet was made!\n")
                    break
                else:
                    print("Sorry, not enough funds")

            except ValueError:
                print("Please, provide integer number")
        return amount

    def dealer_str(self):
        representation = f"{self.name} Hand:"
        representation += f"\n{self.hand[0]}"
        representation += f"\n'Second card'"
        representation += f"\n"
        return representation

    def __str__(self):
        representation = f"{self.name} Hand:"
        for card in self.hand:
            representation += f"\n{card}"
        representation += f"\nScore: {self.score}"
        representation += f"\n"
        return representation


# game setup players
player = PlayerClass(name='Lobster', bank=2000)
dealer = PlayerClass(name='Dealer')

# game logic
game_on = True
while game_on:
    # cleaning screen for the game
    clear_function()

    # cleaning hands from previous cards
    player.clean()
    dealer.clean()

    # creating full new deck of cards
    deck = DeckClass()
    deck.shuffle()

    # asking player for a bet
    bet = player.bet()

    # dealing two cards to the dealer
    for _ in range(2):
        player.get(deck.deal_one())
        dealer.get(deck.deal_one())

    # player turn
    gambling = True
    while gambling:
        print(player)
        print(dealer.dealer_str())

        decision = 'WRONG'
        while decision not in ['Hit', 'Stand']:
            decision = input("Hit or Stand? ")
            if decision not in ['Hit', 'Stand']:
                print("Sorry, I don't understand")

        if decision == 'Hit':
            player.get(deck.deal_one())
            clear_function()
        else:
            gambling = False
            clear_function()

    # computer turn
    if player.score > 21:
        print("Busted!")
        player.money_transfer(-bet)
    else:
        print(dealer)
        time.sleep(3)
        clear_function()

        while dealer.score < 22 and dealer.score < player.score:
            dealer.get(deck.deal_one())
            print(dealer)
            time.sleep(3)
            clear_function()

        # results
        if player.score > dealer.score or dealer.score > 21:
            print(f"{player.name} WINS!")
            player.money_transfer(bet)
        elif player.score < dealer.score:
            print(f"{dealer.name} WINS!")
            player.money_transfer(-bet)
        else:
            print("It's a draw")

    # check for funds
    if player.bank == 0:
        print("Sorry, but you out of money")
        break

    # game continuation
    answer = 'WRONG'
    while answer not in ['Yes', 'No']:
        answer = input(f"{player.name}, do you want to continue? (Yes) or (No) ")
        if answer not in ['Yes', 'No']:
            print("Sorry, I don't understand")

    if answer == 'No':
        break
