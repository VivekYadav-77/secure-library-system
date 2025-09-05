# 📚 Library Management System (Python + SQLite)

This is a **basic Python CLI-based Library Management System** built with SQLite for persistent storage.

---

## 🚀 Features

- User **Registration** and **Login** (with unique User ID)
- View all available and borrowed books
- Borrow books with automatic charge calculation (₹10/day)
- Return books with fine calculation (₹5/day late)
- Persistent storage using **SQLite database**
- Clean and simple CLI interface

---

## ⚙️ Tech Stack

- **Python 3**
- **SQLite3** (built-in Python module)

---

## 📝 Usage

1. Clone the repository  
   ```bash
   git clone https://github.com/VivekYadav-77/secure-library-system.git
   cd librarymanagement
   ```

2. Run the script  
   ```bash
   python librarymanage.py
   ```

3. Options available:
   - Register as a new user (get a unique User ID)
   - Login using your User ID
   - View available books
   - Borrow and return books
   - Logout or Exit

---

## 🔑 Authentication Highlight

- Each user is assigned a **unique User ID** on registration.  
- Borrow and return records are tied to this ID, ensuring proper tracking of books and fines.

---

## 📂 Database Schema

### users
- id (PK)
- name

### books
- id (PK)
- title
- author
- available (1 = available, 0 = borrowed)

### borrows
- id (PK)
- user_id (FK → users.id)
- book_id (FK → books.id)
- borrow_date
- expected_return
- return_date
- charges
- fine

---

## 🧑‍💻 Example Flow

```
--- Library Management ---
1. Register User
2. Login with User ID
3. Exit

Choose option: 1
Enter your name: Rahul
 Registered successfully! Your User ID is 1

--- User Menu (Rahul) ---
1. View Books
2. Borrow Book
3. Return Book
4. Logout
```
