from Credentials import credentials


class AppScripts:

    def __init__(self):
        self.__service = credentials().apps_script
        self.__script_id = "1HVsKmvHS_lx9rcGwxgCDTqFk6hh5BSBQ4RUurRewc8JAha847_8Yqei8"

    def setActiveSelection(self, cell, sheet):
        body = {
            "function": "setActiveSelection",
            "parameters": [
                cell,
                sheet
            ]
        }

        response = self.__service.scripts().run(
            scriptId=self.__script_id,
            body=body).execute()

        print(response)


if __name__ == '__main__':
    AppScripts().setActiveSelection("A1", 1)

