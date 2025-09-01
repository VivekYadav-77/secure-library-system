import sqlite3
from datetime import datetime, timedelta


conn = sqlite3.connect("library.db")
cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    available INTEGER DEFAULT 1
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS borrows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    borrow_date DATE,
    expected_return DATE,
    return_date DATE,
    charges REAL,
    fine REAL DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(book_id) REFERENCES books(id)
)
""")

conn.commit()


cur.execute("SELECT COUNT(*) FROM books")
if cur.fetchone()[0] == 0:
    sample_books = [
        ("Atomic Habits", "James Clear"),
        ("Ikigai", "Héctor García"),
        ("Deep Work", "Cal Newport"),
        ("Rich Dad Poor Dad", "Robert Kiyosaki")
    ]
    cur.executemany("INSERT INTO books (title, author) VALUES (?,?)", sample_books)
    conn.commit()


class User:
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name

    def view_books(self):
        print("\n--- Available Books ---")
        cur.execute("SELECT id, title, author, available FROM books")
        for row in cur.fetchall():
            status = " Available" if row[3] else " Borrowed"
            print(f"[{row[0]}] {row[1]} by {row[2]} - {status}")

    def borrow_book(self, book_id):
        cur.execute("SELECT available, title FROM books WHERE id=?", (book_id,))
        book = cur.fetchone()
        if not book:
            print(" Invalid Book ID.")
            return
        if book[0] == 0:
            print(" Book not available.")
            return

        days = int(input("Enter number of days: "))
        borrow_date = datetime.now()
        expected_return = borrow_date + timedelta(days=days)
        charges = days * 10  

        cur.execute("""
            INSERT INTO borrows (user_id, book_id, borrow_date, expected_return, charges)
            VALUES (?,?,?,?,?)
        """, (self.id, book_id, borrow_date.date(), expected_return.date(), charges))

        cur.execute("UPDATE books SET available=0 WHERE id=?", (book_id,))
        conn.commit()

        print(f" You borrowed '{book[1]}'. Return before {expected_return.date()}. Base charge = ₹{charges}")

    def return_book(self, book_id):
        cur.execute("""
            SELECT id, borrow_date, expected_return, charges 
            FROM borrows 
            WHERE user_id=? AND book_id=? AND return_date IS NULL
        """, (self.id, book_id))
        borrow = cur.fetchone()

        if not borrow:
            print(" No active borrow found for this book.")
            return

        borrow_id, borrow_date, expected_return, charges = borrow
        today = datetime.now().date()

        fine = 0
        if today > datetime.strptime(expected_return, "%Y-%m-%d").date():
            days_late = (today - datetime.strptime(expected_return, "%Y-%m-%d").date()).days
            fine = days_late * 5  

        total = charges + fine

        cur.execute("""
            UPDATE borrows SET return_date=?, fine=? WHERE id=?
        """, (today, fine, borrow_id))
        cur.execute("UPDATE books SET available=1 WHERE id=?", (book_id,))
        conn.commit()

        print(f" Book returned. Charges = ₹{charges}, Fine = ₹{fine}, Total = ₹{total}")

def register_user():
    name = input("Enter your name: ")
    cur.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    user_id = cur.lastrowid
    print(f" Registered successfully! Your User ID is {user_id}")
    return User(user_id, name)

def login_user():
    try:
        user_id = int(input("Enter your User ID: "))
    except ValueError:
        print(" Invalid input.")
        return None

    cur.execute("SELECT id, name FROM users WHERE id=?", (user_id,))
    row = cur.fetchone()
    if row:
        print(f" Welcome back, {row[1]}!")
        return User(row[0], row[1])
    else:
        print(" User not found.")
        return None

def user_menu(user):
    while True:
        print(f"\n--- User Menu ({user.name}) ---")
        print("1. View Books")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. Logout")

        choice = input("Choose option: ")
        if choice == "1":
            user.view_books()
        elif choice == "2":
            try:
                book_id = int(input("Enter Book ID to borrow: "))
                user.borrow_book(book_id)
            except ValueError:
                print(" Invalid input.")
        elif choice == "3":
            try:
                book_id = int(input("Enter Book ID to return: "))
                user.return_book(book_id)
            except ValueError:
                print(" Invalid input.")
        elif choice == "4":
            print("👋 Logging out...")
            break
        else:
            print(" Invalid choice.")


def main():
    while True:
        print("\n--- Library Management ---")
        print("1. Register User")
        print("2. Login with User ID")
        print("3. Exit")

        choice = input("Choose option: ")
        if choice == "1":
            user = register_user()
            user_menu(user)
        elif choice == "2":
            user = login_user()
            if user:
                user_menu(user)
        elif choice == "3":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print(" Invalid choice.")

if __name__ == "__main__":
    main()
