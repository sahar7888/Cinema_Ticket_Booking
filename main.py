
""" Ref: Intermediate to Advanced Python with 10 OOP Projects-Udemy
"""




import sqlite3
import webbrowser
from fpdf import FPDF
from cardinfo import CardInfo
from tablecreation import Creator

class Seat(Creator):
    def __init__(self, seat, name):
        self.seat = seat
        self.name = name

    def is_free(self):
        connection = Creator.database
        cursor = connection.cursor()
        cursor.execute("""
                SELECT "seat_id" FROM "Seat" WHERE "taken"==0
                """)
        result = cursor.fetchall()
        print("The following seats are free!: " + str(result))

    def availability(self):

        connection = self.database
        cursor = connection.cursor()
        cursor.execute("""
          SELECT "taken" FROM "Seat" WHERE "seat_id" = ?
          """, [self.seat])
        self.seatavail = cursor.fetchall()[0][0]
        if self.seatavail == 0:
            self.buy_ticket()
        else:
            print("Seat is occupied, please try another seat")

    def buy_ticket(self):
        connection = self.database
        cursor = connection.cursor()
        cursor.execute("""
           SELECT "balance" FROM "Banking" WHERE "user"= ?
           """, [self.name])
        self.balance = float(cursor.fetchone()[0])
        cursor.execute("""
           SELECT "price" FROM "Seat" WHERE "seat_id" = ?
           """, [self.seat])
        self.ticketprice = float(cursor.fetchone()[0])

        if self.balance > self.ticketprice:
            print("Ticket purchase succesful!")
        else:
            print("Not enough balance")

        self.banking_operations()


    def banking_operations(self):

        newbalance = self.balance - self.ticketprice
        connection = self.database
        connection.execute("""
        UPDATE "Banking" SET "balance"=? WHERE "user"=?
        """, [newbalance, self.name])
        connection.commit()
        ticket =  PdfTicket(self.name, self.ticketprice, self.seat, newbalance)
        ticket.generate()
        print("Generating ticket...")


class PdfTicket:

    def __init__(self, user, priceticket, seat_number, remainbalance):
        self.user = user
        self.priceticket = priceticket
        self.seat_number = seat_number
        self.remainbalance = remainbalance

    def generate(self):
        ticketprice = str(round(self.priceticket, 2))
        remaining = str(round(self.remainbalance, 2))

        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        pdf.set_font(family='Times', size=24, style='B')
        pdf.cell(w=0, h=80, txt="Enjoy the movie!", border=0, align="C", ln=1)

        pdf.set_font(family="Times", size=12, style='B')
        pdf.cell(w=100, h=40, txt="Name: ", border=0)
        pdf.cell(w=100, h=40, txt=self.user, border=0, ln=1)

        pdf.set_font(family="Times", size=12, style='B')
        pdf.cell(w=100, h=40, txt="Price: ", border=0)
        pdf.cell(w=100, h=40, txt=ticketprice, border=0, ln=1)

        pdf.set_font(family="Times", size=12, style='B')
        pdf.cell(w=100, h=40, txt="Seat Number: ", border=0)
        pdf.cell(w=100, h=40, txt=str(self.seat_number), border=0, ln=1)

        pdf.set_font(family="Times", size=12, style='B')
        pdf.cell(w=100, h=40, txt="Balance: ", border=0)
        pdf.cell(w=150, h=40, txt=remaining, border=0, ln=1)

        pdf.output("cinema.pdf", 'F')
        webbrowser.open("cinema.pdf")

# Checks for free seats
free = Seat("free", "seats")
free.is_free()

# For new users, comment the below inputs if not a new user

cardtype = input("Enter your card type: ")
cardnumber = input("Enter your card number: ")
cvc = input("Enter your card's security code: ")
holder = input("Name displayed on your card: ")
balance = input("Credit amount you 'd like to use: ")
cardinfo = CardInfo(cardtype, cardnumber, cvc, holder, balance)
cardinfo.new_user_card()


# For already registered Users

seat = input("Enter your preffered seat:")
name = input("Enter your username: ")
buytick = Seat(seat, name)

buytick.availability()

