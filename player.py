"""

"""
import socket

SIZE = 1024

class client:
    def __init__(self):
        """
        socket,
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.connect((socket.gethostname(),8080))
        self.current_card = ""

    def game(self):
        """
        recieve message and respond
        """
        flag = True
        while(flag):
            self.turn()

    def turn(self):
        """
        take one turn
        """
        msg = self.sock.recv(SIZE)
        inp = input(msg)
        self.sock.send(inp.encode())



    def main(self):
        self.game()

if __name__ == "__main__":
    p = client()
    p.main()
