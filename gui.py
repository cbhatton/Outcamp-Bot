import json
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from typing import Optional


class Gui(Tk):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, connection=None):
        if self.__initialized:
            return
        self.__connection = connection

        self.__initialized = True
        Tk.__init__(self)

        self.__mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.__mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.title = self.title("OUTCAMP BOT")

        # variables
        self._sheet = StringVar()
        self._message = StringVar()
        self._creds_file = StringVar()

        self.main_window()
        self.mainloop()

    def main_window(self):
        self.refresh()

        ttk.Label(self.__mainframe, textvariable=self._message).grid(column=2, row=2, sticky=(W, E, N, S))
        self._message.set("WELCOME TO OUTCAMP! START SCANNING TO BEGIN")

        ttk.Button(self.__mainframe, text="settings", command=self.get_credentials).grid(column=3, row=3, sticky="SE")

    def display_message(self, m: str):
        self._message.set(m)

    def get_credentials(self):
        self.refresh()

        ttk.Label(self.__mainframe, textvariable="sheet_id").grid(column=1, row=1, columnspan=10, sticky=(W, E))

        sheet_entry = ttk.Entry(self.__mainframe, width=7, textvariable=self._sheet)
        sheet_entry.grid(column=1, row=1, sticky=(W, E))

        ttk.Button(self.__mainframe, text="upload file", command=self.upload).grid(column=1, row=2, sticky="NSEW")

        ttk.Button(self.__mainframe, text="Apply settings", command=self.apply_settings).grid(column=1, row=3, sticky=W)

    """Helper Functions"""
    def upload(self):
        self._creds_file = filedialog.askopenfilename()

    def apply_settings(self):
        """Set sheet id"""
        if len(self._sheet.get()) > 1:
            settings = {"sheet_id": self._sheet.get()}

            with open("./settings.json", 'w') as f:
                json.dump(settings, f)

        """Set credentials file"""
        if isinstance(self._creds_file, StringVar):
            self._creds_file = ""
        if len(self._creds_file) > 1:
            try:
                try:
                    os.remove('./token.json')
                except WindowsError as e:
                    pass
                with open(self._creds_file.get(), 'r') as creds:
                    if '.json' not in creds:
                        self.show_message("credentials file must be type json, try again")
                        raise TypeError
                    with open('credentials.json', 'w') as f:
                        json.dump(creds, f)
            except Exception as e:
                print(e)

        self.__connection.refresh_sheet(self._sheet.get())
        self.main_window()

    def refresh(self):
        self.__mainframe.destroy()

        self.__mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.__mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


if __name__ == '__main__':

    Gui().get_credentials()