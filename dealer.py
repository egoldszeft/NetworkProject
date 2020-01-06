import socket #server
import random
import select
from threading import Thread
SIZE = 1024
class game:
    #constructor that initializes the deck and earnings
    def __init__(self, client_socket):
        self.round = 0
        self.earnings = 0
        self.client_socket = client_socket
        self.deck = [["2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC"],
                     ["2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD"],
                     ["2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AH"],
                     ["2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AS"]]
    #function rollCard randomly chooses one card from the deck and leaves a grave instead of it
    #recieves: self
    #returns: a card in string form and its position in the deck in integers
    def rollCard(self):
        i = random.randint(0,3)
        j = random.randint(0,12)
        while self.deck[i][j] == 0:
            i = random.randint(0,3)
            j = random.randint(0,12)
        card = self.deck[i][j]
        self.deck[i][j] = 0
        return card , i , j
    # thread method
    #recieve activates as soon as the connection is initiated and sends the firstcard.
    # then handles various cases of the turn, (win,loss,etc)
    def turn(self):
        card1, i1, j1 = self.rollCard()
        self.client_socket.send(("First card is " + card1 + " how much would you like to bet? ").encode())
        bet = int(self.client_socket.recv(SIZE))
        if bet > 0:
            card2, i2, j2 = self.rollCard()
            winner = self.calcWinner(j1, j2)
        if winner == "Tie":
            self.client_socket.send(("The result of round"+ str(self.round) +"is a tie! \n Dealer's card: " + card2 + "\n Player's card: " + card1 + "\n The bet: " + str(bet) + "$ \n Do you wish to go to surrender or go to war").encode())
            choice = self.client_socket.recv(SIZE)
            if choice == "Surrender":
                self.earnings -= bet / 2
            if choice == "War":
                self.rollCard()
                self.rollCard()
                self.rollCard()
                card1, i1, j1 = self.rollCard()
                card2, i2, j2 = self.rollCard()
                winner = self.calcWinner(j1, j2)
                if winner == "Tie":
                    self.earning += bet * 2
                    self.client_socket.send(("Round" + str(self.round) + "tie breaker: \n" + "Going to war! \n 3 cards were discarded. \n Original bet: " + str(bet) + "$\n New bet: " +str(bet*2) +
                        "\n Dealer's card:" + card1 + "\n Player's card: "+ card2 + "player won:" + str(bet*2) + "$\n").encode())

                if winner == "Player":
                    self.earnings += bet
                    self.client_socket.send(("Round" + str(self.round) + "tie breaker: \n" + "Going to war! \n 3 cards were discarded. \n Original bet: " + str(bet) + "$\n New bet: " +str(bet*2) +
                        "\n Dealer's card:" + card1 + "\n Player's card: "+ card2 + "player won:" + str(bet) + "$\n").encode())
                if winner == "Dealer":
                    self.earnings -= bet * 2
                    self.client_socket.send(("Round" + str(self.round) + "tie breaker: \n" + "Going to war! \n 3 cards were discarded. \n Original bet: " + bet + "$\n New bet: " +bet*2 +
                        "\n Dealer's card:" + card1 + "\n Player's card: "+ card2 + "Dealer won:" + bet*2 + "$\n").encode())
                return
        if winner == "Player":
            self.earnings += bet
            self.client_socket.send(("Round" + str(self.round) + "Original bet: +" + str(bet)+ "Dealer's card:" + card1 + "Player's card: " + card2 + "Players won:" + str(bet) + "$").encode())
        if winner == "Dealer":
            self.earnings -= bet
            self.client_socket.send(("Round" + str(self.round) + "Original bet: +" + str(bet) + "Dealer's card:" + card1 + "Player's card: " + card2 + "Dealer won:" + str(bet) + "$").encode())
    def doGame(self):
        msg = "start"
        while msg == "start":
            self.turn()
            self.client_socket.send(("Do you wish to continue").encode())
            choice = self.client_socket.recv(SIZE)
            if str(choice) == "no" or str(choice) == "No":
                    msg = "no"

    #function isEmpty fully checks wether or not the deck in the currenct game is empty
     #recieves: self
     #returns: boolean: true if the deck is empty and false if not
    def isEmpty(self): #function that checks wether or not the array is fully 0
        i = 0
        j = 0
        while i < 4:
            while j < 13:
                if self.deck[i][j] != 0:
                    return False
        return True


    #function calcWinner recieves the two numbers drawn and then returns a string of the winner
    #recieves: self , integers symbolyzing the numbers drawn
    #returns: string: if player won "Player" , if dealer won "Dealer" else "Tie"
    def calcWinner(self , j1  , j2):
        if j1 == j2:
            return "Tie"
        if j1 < j2 :
            return "Dealer"
        if j1 > j2:
            return "Player"





class dealer:
    global game1
    global game2
    def __init__(self):
        self.active_players = ([0 , 0])
    def main(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((socket.gethostname(),8080))
        server.listen(5)
        while True:
            conn , addr = server.accept()
            if self.active_players[0] == 1:
                if self.active_players[1] == 1:
                    conn.send("occupied".encode())
                    conn.close()
                else:
                    self.game2 = game(conn)
                    self.active_players[1] = 1
                    threader = Thread(target= self.game2.doGame , daemon = True)
                    threader.start()
            else:
                self.game1 = game(conn)
                self.active_players[0] = 1
                threader2 = Thread(target=self.game1.doGame,daemon = True)
                threader2.start()


if __name__ == "__main__":
    d = dealer()
    d.main()