import json
import secrets

import ndef
import nfc

from Sheet import Sheet
from gui import Gui


class Connection:

    def __init__(self):
        with open('settings.json', 'r') as f:
            settings = f.readline()
            settings = json.loads(settings)

        self.__sheet = Sheet(settings["sheet_id"])
        self.__clf = nfc.ContactlessFrontend()

        assert self.__clf.open('usb') is True

    def wait_for_tag(self):

        tag = self.__clf.connect(rdwr={'on-connect': lambda tag: False})
        print(tag)

        if len(tag.ndef.records) == 0:
            token = secrets.token_hex(8)

            tag.ndef.records = [ndef.TextRecord(token)]
            print(tag.ndef.records)
            self.__sheet.add_row(token)
        else:
            token = tag.ndef.records[0].text
            print(token)
            row = self.__sheet.find_tag_id(token)

            print(row)

            self.__sheet.float_row(row)

        Gui().display_message(f'Tag ID: {token}')

    def main(self):
        while True:
            try:
                print('Running')
                self.wait_for_tag()
            except Exception as e:
                print(e)
                Gui().display_message("Error")
                self.main()

    def refresh_sheet(self, id: str):
        # checks
        if len(id) < 1:
            Gui().display_message("Enter valid sheet id")
            raise ValueError

        self.__sheet = Sheet(id)


if __name__ == '__main__':
    sheet = Sheet('1UXQ1YRHduKlEbhRDUChRh1D-F2ln75VLQ9c7yE_69BU')

    Connection().wait_for_tag()
