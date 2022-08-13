from threading import Thread
from connection import Connection

from gui import Gui

class Main:

    @staticmethod
    def main():
        connection = Connection()

        connection_thread = Thread(target=connection.main)

        connection_thread.start()
        print('connection thread started')
        Gui(connection=connection).mainloop()




if __name__ == '__main__':
    Main().main()

