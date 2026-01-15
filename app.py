import mysql.connector
from datetime import date

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_mysql_password",   # change this
    database="library_db"
)

cursor = db.cursor()

def add_book():
    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    quantity = int(input("Enter Quantity: "))
    cursor.execute("INSERT INTO books (title, author, quantity) VALUES (%s,%s,%s)", 
                   (title, author, quantity))
    db.commit()
    print("Book added successfully!")

def add_member():
    name = input("Enter Member Name: ")
    email = input("Enter Member Email: ")
    cursor.execute("INSERT INTO members (name, email) VALUES (%s,%s)", 
                   (name, email))
    db.commit()
    print("Member added successfully!")

def issue_book():
    book_id = int(input("Enter Book ID: "))
    member_id = int(input("Enter Member ID: "))
    
    cursor.execute("SELECT quantity FROM books WHERE book_id=%s", (book_id,))
    result = cursor.fetchone()
    
    if result and result[0] > 0:
        cursor.execute("INSERT INTO issued_books (book_id, member_id, issue_date) VALUES (%s,%s,%s)",
                       (book_id, member_id, date.today()))
        cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id=%s", (book_id,))
        db.commit()
        print("Book issued successfully!")
    else:
        print("Book not available!")

def return_book():
    issue_id = int(input("Enter Issue ID: "))
    
    cursor.execute("SELECT book_id FROM issued_books WHERE issue_id=%s AND return_date IS NULL", (issue_id,))
    result = cursor.fetchone()
    
    if result:
        book_id = result[0]
        cursor.execute("UPDATE issued_books SET return_date=%s WHERE issue_id=%s", (date.today(), issue_id))
        cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id=%s", (book_id,))
        db.commit()
        print("Book returned successfully!")
    else:
        print("Invalid Issue ID or already returned!")

def view_books():
    cursor.execute("SELECT * FROM books")
    for row in cursor.fetchall():
        print(row)

def view_members():
    cursor.execute("SELECT * FROM members")
    for row in cursor.fetchall():
        print(row)

def menu():
    while True:
        print("\n===== Library Database Management =====")
        print("1. Add Book")
        print("2. Add Member")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. View Books")
        print("6. View Members")
        print("7. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            add_book()
        elif choice == '2':
            add_member()
        elif choice == '3':
            issue_book()
        elif choice == '4':
            return_book()
        elif choice == '5':
            view_books()
        elif choice == '6':
            view_members()
        elif choice == '7':
            break
        else:
            print("Invalid choice!")

menu()
