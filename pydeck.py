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

#hand extends Deck (it is a type of deck). Both are a set of
#cards and bothe support like oppertations (e.g. adding cards, removing cards)
#a hand also supports operations that a deck does not (i.e. classifying a poker hand)
#so we derive hand from deck vi inheritance.

class Hand(Deck):
    #we initialize and empty list to contain the card set and name to designate the 
    #player to whom the specific hand is dealt - hand inherits printHand and overides
    #__str__ from deck
    def __init__(self, name=""):
        self.cards = []
        self.name = name

    #when overiding __str__ from deck it is legal to pass hand because hand is a type
    #of deck. if the hand is not empty it passes itself to deck and invokes the __str__
    #method of deck
    def __str__(self):
        s = "Hand " + self.name
        if self.isEmpty():
            return s + " is empty\n"
        else:
            return s + " contains\n" + Deck.__str__(self)
    
    #hand inherits remove from deck.
    def addCard(self,card):
            self.cards.append(card)


#the CardGame instantiates and shuffles a deck it generally takes care of chores common
#to all card games. othere card games (e.g.poker, old maid) can inherit from CardGame 

class CardGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

#the OldMaidHand is a type of Hand specific to old maid. it inherits from hand and adds
#the removeMatches method. here is a sample invocation:
#cg = CardGame()
#h = OldMaidHand('jody')
#cg.deck.deal([h], 26)
#print h
#h.removeMatches()

class OldMaidHand(Hand):
    def removeMatches(self):
        count = 0
        #copy the list for traversal - self.cards gets modified
        originalCards = self.cards[:]
        for card in originalCards:
            #3 - card.suit turns a Club (suit 0) into a Spade (suit 3)
            #and a Diamond (suit 1) into a Heart (suit 2).
            match = Card(3 - card.suit, card.rank)
            if match in self.cards:
                self.cards.remove(card)
                self.cards.remove(match)
                print "Hand %s: %s matches %s" % (self.name,card,match)
                count = count + 1
        return count

#OldMaidGame is a type of Card Game specific to old maid. here is a 
#sample invocation:
#from pydeck import *
#g = OldMaidGame()
#g.play(['foo', 'bar', 'bash'])

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

        # play until all 50 cards are matched.
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
