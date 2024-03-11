import sqlite3


class Creator:
    database = sqlite3.connect("cinema.db")

    @classmethod
    def create_user_table(self):
        connection = self.database
        connection.execute("""
        CREATE TABLE "Card Information"(
            "type" TEXT,
            "number" TEXT,
            "cvc" TEXT,
            "holder" TEXT,
            "balance" REAL
        );
        """)

    @classmethod
    def create_seat(self):
        connection = self.database
        connection.execute("""
        CREATE TABLE "Seat" (
            "seat_id" TEXT,
            "taken" INTEGER,
            "price" REAL
        );
        """)

    def create_banking_table(self):
        connection = self.database
        connection.execute("""
        CREATE TABLE "Banking"(
            "user" TEXT,
            "balance" REAL
        );
        """)

    def insert_seats(self, seat_id, occupied, price):
        connection = sqlite3.connect(self.database)
        connection.execute("""
               INSERT INTO "Seat" (seat_id, taken, price)
               VALUES (?, ?, ?)""", (seat_id, occupied, price))
        connection.commit()
        connection.close()





