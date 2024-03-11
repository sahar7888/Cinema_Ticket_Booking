import sqlite3
from tablecreation import Creator


class CardInfo (Creator):
    database = Creator.database
    def __init__(self, type, number, cvc, holder, balance):
        self.type = type
        self.number = number
        self.cvc = cvc
        self.holder = holder
        self.balance = balance

    def new_user_card(self):
        connection = self.database
        connection.execute("""
         INSERT INTO "Card Information" (type, number, cvc,
         holder, balance)
         VALUES (?, ?, ?, ?, ?)""", (self.type, self.number,
                                     self.cvc, self.holder, self.balance))
        connection.commit()
        self.banking_user()



    def banking_user(self):
        connection = self.database
        connection.execute("""
        INSERT INTO "Banking" (user, balance)
        VALUES (?, ?)""", (self.holder, self.balance))
        connection.commit()
