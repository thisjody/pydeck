#!/usr/bin/python
#Object oriented card deck written in python
#The Card object currently configured for a 52 card playig deck
#Change suitlist and rank list to create Tarot or other deck
#suitlist is indexed 0 to 3 begining with clubs (eg Clubs=0, Spades=3)

class Card:
    #class attributes for mapping - narf is a place holder for 0
    #because it is more natural to index cards to their real values
    #(eg Ace=1 rather than 0)

    suitList = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rankList = ["narf", "Ace", "2", "3", "4", "5", "6", "7",
            "8", "9", "10", "Jack", "Queen", "King"]

    #we initialize a default 2 of clubs if suit and rank are not declared
    #explicitly when the card is instantiated
    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank
    
    #the string method uses rank and suit to index into the ranklist and
    #suit list to produce human readable card suits and ranks
    def __str__(self):
        return (self.rankList[self.rank] + " of " +
                self.suitList[self.suit])

    def __cmp__(self, other):
        # check the suits
        if self.suit > other.suit: return 1
        if self.suit < other.suit: return -1
        # suits are the same... check ranks
        if self.rank > other.rank: return 1
        if self.rank < other.rank: return -1
        # ranks are the same... it's a tie
        return 0

#The Deck shuffles, deals, and prints 

class Deck:
    #The deck is populated with a nested loop (0 to 3 and 1 to 14)
    #each pass instatiates a new card with the current list rank and 
    #appends it to the cards list
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))

    #the ""*i multiplies space times the current value of the i to create
    #cascade when we print the cards. s is an accumulator gathering the cards
    def __str__(self):
        s = ""
        for i in range(len(self.cards)):
            s = s + " "*i + str(self.cards[i]) + "\n"
        return s

    #traverse the cards and swap each card with a random card. a card can be swapped
    #with itself. we get the actual length of the list and store it in nCards. this
    #accomodates decks of vsrious sizes as an uper bound.
    def shuffle(self):
        import random
        nCards = len(self.cards)
        for i in range(nCards):
            j = random.randrange(i, nCards)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]


    #we use the in operator to check for deep equality
    def removeCard(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False

    #pop a card from the bottom of the deck
    def popCard(self):
        return self.cards.pop()

    #check for an empty deck
    def isEmpty(self):
        return (len(self.cards) == 0)

    
    def deal(self, hands, nCards=999):
        nHands = len(hands)
        for i in range(nCards):
            if self.isEmpty(): break # break if out of cards
            card = self.popCard() # take the bottom card
            hand = hands[i % nHands] # whose turn is next?
            hand.addCard(card) # add the card to the hand

#The Hand extends Deck (it is a type of deck). 

class Hand(Deck):
    def __init__(self, name=""):
        self.cards = []
        self.name = name

    def __str__(self):
        s = "Hand " + self.name
        if self.isEmpty():
            return s + " is empty\n"
        else:
            return s + " contains\n" + Deck.__str__(self)

    def addCard(self,card):
            self.cards.append(card)


#The CardGame instantiates and shuffles a deck

class CardGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

#The OldMaidHand is a type of hand specific to Old Maid

class OldMaidHand(Hand):
    def removeMatches(self):
        count = 0
        originalCards = self.cards[:]
        for card in originalCards:
            match = Card(3 - card.suit, card.rank)
            if match in self.cards:
                self.cards.remove(card)
                self.cards.remove(match)
                print "Hand %s: %s matches %s" % (self.name,card,match)
                count = count + 1
        return count

#The OldMaidGame is a type of Card Game specific to Old Maid

class OldMaidGame(CardGame):
    def play(self, names):
        # remove Queen of Clubs
        self.deck.removeCard(Card(0,12))

        # make a hand for each player
        self.hands = []
        for name in names :
            self.hands.append(OldMaidHand(name))

        # deal the cards
        self.deck.deal(self.hands)
        print "---------- Cards have been dealt"
        #self.printHands()

        # remove initial matches
        matches = self.removeAllMatches()
        print "---------- Matches discarded, play begins"
        #self.printHands()

        # play until all 50 cards are matched
        turn = 0
        numHands = len(self.hands)
        while matches < 25:
            matches = matches + self.playOneTurn(turn)
            turn = (turn + 1) % numHands

        print "---------- Game is Over"
        self.printHands()

    def removeAllMatches(self):
        count = 0
        for hand in self.hands:
            count = count + hand.removeMatches()
            return count

    def printHands(self):
        for hand in self.hands:
            print hand

    def playOneTurn(self, i):
        if self.hands[i].isEmpty():
            return 0
        neighbor = self.findNeighbor(i)
        pickedCard = self.hands[neighbor].popCard()
        self.hands[i].addCard(pickedCard)
        print "Hand", self.hands[i].name, "picked", pickedCard
        count = self.hands[i].removeMatches()
        self.hands[i].shuffle()
        return count


    def findNeighbor(self, i):
        numHands = len(self.hands)
        for next in range(1,numHands):
            neighbor = (i + next) % numHands
            if not self.hands[neighbor].isEmpty():
                return neighbor
