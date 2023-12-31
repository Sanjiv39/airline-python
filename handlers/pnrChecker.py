from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
import sqlite3, re

class PnrChecker:
    def validatePnr(self, obj):
        inputBox = obj[0]
        pnr_number = inputBox.text
        special_char = re.compile('[^a-zA-Z\d\s:]')
        x = False
        # check user_input PNR
        if(len(pnr_number)==0):
            inputBox.error = True
            inputBox.helper_text = 'Required'
            # x = False
        elif (special_char.search(pnr_number)!=None):
            inputBox.error = True
            inputBox.helper_text = 'PNR can only contain alphanumeric characters'
            # x = False
        elif not re.match("^[a-zA-Z0-9]+$", pnr_number):
            inputBox.error = True
            inputBox.helper_text = 'PNR contains spaces in between'
            # x = False
        elif(len(pnr_number) != 6):
            inputBox.error = True
            inputBox.helper_text = 'PNR must be 6 characters only'
            # x = False
        else:
            if obj[1]:
                data = self.check_database_for_pnr(pnr_number)
                if data != []:
                    # data = data[0]
                    x = data
                else:
                    x = []
                    inputBox.error = True
                    inputBox.helper_text = 'No such PNR exists please add correct PNR'

        return x

    def check_database_for_pnr(self, pnr_number):
        conn = sqlite3.connect("./data/database.db")
        
        # create cursor for cmds
        c = conn.cursor()

        # execute cmd for credentials table
        c.execute("SELECT * FROM tickets WHERE pnr_id = (:pnr)", {
            "pnr": pnr_number.upper()
        })
        record = c.fetchall()

        # commit and close 
        conn.commit()
        conn.close()

        return record

if __name__ == "__main__":
    PnrChecker().run()
