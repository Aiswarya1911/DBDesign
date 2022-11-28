import tkinter as tk
from datetime import timedelta, date
from tkinter import *
from tkinter import ttk, simpledialog
from tkinter import messagebox
from tkinter.ttk import Treeview

import mysql.connector

LARGE_FONT = ("calibre", 12)
Login_username = 'library'
Login_password = 'mydb'
LibraryDB = mysql.connector.connect(**{'user': 'root', 'password': 'root', 'host': 'localhost', 'db': 'library'})


def GenerateMessage(Msg):
    tk.messagebox.showinfo("LMS", Msg)


class LibraryUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.geometry('800x700')
        self.title("Library Management System")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (LogInPage, MainPage, BookSearchPage, BorrowerPage, CheckInPage, PayFines):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LogInPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def Validate_LogIn(uname, pwrd, controller):
    if uname.get() == Login_username and pwrd.get() == Login_password:

        if LibraryDB.is_connected():
            # print("DB is connected")
            controller.show_frame(MainPage)

    else:
        # print("Invalid username or password")
        GenerateMessage("Invalid credentials...Try Again")


class LogInPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        HeadingLabel = Label(self, text="Welcome to Library Management System", font=('calibre', 20, 'normal'))
        HeadingLabel.place(x=150, y=100)

        UserNameLabel = ttk.Label(self, text="UserName", font=('calibre', 10, 'normal'))
        UserNameLabel.place(x=200, y=350)

        uname = StringVar()
        UserNameEnter = ttk.Entry(self, textvariable=uname)
        UserNameEnter.place(x=300, y=350)

        PasswordLabel = ttk.Label(self, text="Password", font=('calibre', 10, 'normal'))
        PasswordLabel.place(x=200, y=400)

        pwrd = StringVar()
        PasswordEntry = ttk.Entry(self, textvariable=pwrd, show='*')
        PasswordEntry.place(x=300, y=400)

        LoginBtn = ttk.Button(self, text="Login",
                              command=lambda: Validate_LogIn(uname, pwrd, controller))
        LoginBtn.place(x=300, y=500)

        ExitBtn = ttk.Button(self, text="Exit",
                             command=lambda: Tk.quit(parent))
        ExitBtn.place(x=300, y=550)


def addBorrower(ssn, Address, City, State, Fname, Lname, PhNo):
    cursor = LibraryDB.cursor()

    cursor.execute("SELECT COUNT(CardID) from BORROWERS")
    new_card_no = int(cursor.fetchall()[0][0]) + 1
    new_card_no = 'ID00' + str(new_card_no)
    cursor.execute("SELECT EXISTS(SELECT Ssn FROM BORROWERS WHERE BORROWERS.ssn = '" + str(ssn) + "')")
    result = cursor.fetchall()
    if result == [(0,)]:
        address = ', '.join([Address.get(), City.get(), State.get()])
        bname = ' '.join([Fname.get(), Lname.get()])
        cursor.execute(
            "Insert into BORROWERS (CardID, ssn,bname, address, phone) Values ('" + new_card_no + "', '" + str(
                ssn.get()) + "', '" + str(
                bname) + "', '" + str(address) + "', '" + str(PhNo.get()) + "')")
        LibraryDB.commit()
        GenerateMessage("Added Borrower")
    else:
        GenerateMessage("Error, Borrower Already Exists!")


class BorrowerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titleLabel = Label(self, text="Enter Details")
        titleLabel.grid(row=0, column=0, padx=20, pady=20)
        fnameLabel = Label(self, text="First Name").grid(row=1, column=0, padx=10, pady=5)
        fnameTB = Entry(self)
        fnameTB.grid(row=1, column=2, padx=10, pady=5)
        lnameLabel = Label(self, text="Last Name").grid(row=3, column=0, padx=10, pady=5)
        lnameTB = Entry(self)
        lnameTB.grid(row=3, column=2, padx=10, pady=5)
        ssnLabel = Label(self, text="SSN").grid(row=5, column=0, padx=10, pady=5)
        ssnTB = Entry(self)
        ssnTB.grid(row=5, column=2, padx=10, pady=5)
        addressLabel = Label(self, text="Street Address").grid(row=7, column=0, padx=10, pady=5)
        addressTB = Entry(self)
        addressTB.grid(row=7, column=2, padx=10, pady=5)
        cityLabel = Label(self, text="City").grid(row=9, column=0, padx=10, pady=5)
        cityTB = Entry(self)
        cityTB.grid(row=9, column=2, padx=10, pady=5)
        stateLabel = Label(self, text="State").grid(row=11, column=0, padx=10, pady=5)
        stateTB = Entry(self)
        stateTB.grid(row=11, column=2, padx=10, pady=5)
        numberLabel = Label(self, text="Phone Number").grid(row=13, column=0, padx=10, pady=5)
        numberTB = Entry(self)
        numberTB.grid(row=13, column=2, padx=10, pady=5)
        addBtn = Button(self, text="Add", width=30,
                        command=lambda: addBorrower(ssnTB, addressTB, cityTB, stateTB, fnameTB, lnameTB, numberTB))
        addBtn.grid(row=14, column=0, padx=10, pady=5)
        BackButton = ttk.Button(self, text="Back To HomePage", width=40,
                                command=lambda: controller.show_frame(MainPage))
        BackButton.grid(row=18, column=2)
        BackButton.grid_rowconfigure(2, weight=1)


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        HeadingLabel = Label(self, text="Select your Option....", font=('calibre', 15, 'normal'))
        HeadingLabel.place(x=250, y=100)
        BookSearchBtn = ttk.Button(self, text="Search   ", width=30,
                                   command=lambda: controller.show_frame(BookSearchPage))
        BookSearchBtn.place(x=300, y=250)
        CheckInBtn = ttk.Button(self, text="Checkin ", width=30, command=lambda: controller.show_frame(CheckInPage))
        CheckInBtn.place(x=300, y=300)
        BorroweBtn = ttk.Button(self, text="Add Borrower", width=30,
                                command=lambda: controller.show_frame(BorrowerPage))
        BorroweBtn.place(x=300, y=350)
        FinesBtn = ttk.Button(self, text="Pay Fines", width=30, command=lambda: controller.show_frame(PayFines))
        FinesBtn.place(x=300, y=400)
        LogOutBtn = ttk.Button(self, text="LogOut", width=30, command=lambda: controller.show_frame(LogInPage))
        LogOutBtn.place(x=300, y=450)


class CheckInPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.bookForCheckInID = None
        self.search_string = None
        self.data = None
        searchLabel = ttk.Label(self, text="Search here: Borrower ID, Borrower Name or ISBN")
        searchLabel.grid(row=0, column=0, padx=20, pady=20)
        searchTextBox = ttk.Entry(self)
        searchTextBox.grid(row=1, column=0)
        self.search_string = searchTextBox.get()
        searchBtn = ttk.Button(self, text="Search", command=lambda: self.search_book_loans())
        searchBtn.grid(row=2, column=0)
        self.table = Treeview(self, columns=["Loan ID", "ISBN", "Borrower ID", "Title"])
        self.table.grid(row=3, column=0)
        self.table.heading('#0', text="Loan ID")
        self.table.heading('#1', text="ISBN")
        self.table.heading('#2', text="Borrower ID")
        self.table.heading('#3', text="Book Title")
        self.table.bind('<ButtonRelease-1>', self.select_book_for_checkin)
        checkInBtn = ttk.Button(self, text="Check In", command=self.check_in)
        checkInBtn.grid(row=4, column=0)
        BackButton = ttk.Button(self, text="Back To HomePage", width=40,
                                command=lambda: controller.show_frame(MainPage))
        BackButton.grid(row=30, column=0)
        BackButton.grid_rowconfigure(5, weight=1)

    def search_book_loans(self):
        search_b = "'%" + self.search_string + "%'"
        # print(search_b)
        cursor = LibraryDB.cursor()
        cursor.execute(
            "select BOOK_LOANS.Loan_Id, BOOK_LOANS.ISBN, BOOK_LOANS.Card_id, BOOK.title, BOOK_LOANS.Date_in "
            "from BOOK_LOANS "
            "join BORROWERs on BOOK_LOANS.Card_id = BORROWERs.CardID "
            "join BOOK on BOOK_LOANS.ISBN = BOOK.ISBN "
            "where Borrowers.CardID like " + search_b + " or Borrowers.Bname like " + search_b + " or Book.Isbn like " + search_b)

        self.data = cursor.fetchall()
        # for row in self.data:
        #     print(row)
        self.view_data()

    def view_data(self):
        """
            View data on Treeview method.
            """
        self.table.delete(*self.table.get_children())
        for elem in self.data:
            if elem[4] is None:
                self.table.insert('', 'end', text=str(elem[0]), values=(elem[1], elem[2], elem[3]))

    def select_book_for_checkin(self, a):
        curItem = self.table.focus()
        self.bookForCheckInID = self.table.item(curItem)['text']
        #print("Loan Id to be checked out:" + self.bookForCheckInID)

    def check_in(self):
        today = date.today()
        if self.bookForCheckInID is None:
            GenerateMessage("Attention!, Select Book to Check In First!")
            return None
        cursor = LibraryDB.cursor()
        cursor.execute("SELECT BOOK_LOANS.Date_in FROM BOOK_LOANS WHERE BOOK_LOANS.Loan_Id = '" + str(
            self.bookForCheckInID) + "'")
        result = cursor.fetchall()
        # print(result[0][0])
        if result[0][0] is None:
            cursor.execute("UPDATE BOOK_LOANS SET BOOK_LOANS.Date_in = '" + str(
                today) + "' WHERE BOOK_LOANS.Loan_Id = '"
                           + str(self.bookForCheckInID) + "'")
            LibraryDB.commit()
            GenerateMessage("Done, Book Checked In Successfully!")

        else:
            return None


class BookSearchPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.bookIsbn = None
        self.borrowerId = None
        SearchTextBox = ttk.Entry(self, width=60)
        SearchTextBox.grid(row=1, column=2)
        SearchTextBox.grid_rowconfigure(0, weight=1)
        SearchButton = ttk.Button(self, text='Search', command=lambda: self.SearchBook(SearchTextBox))
        SearchButton.grid(row=2, column=2)
        SearchButton.grid_rowconfigure(1, weight=1)
        CheckOutBtn = ttk.Button(self, text="CheckOut", width=30, command=lambda: self.BookCheckOut())
        CheckOutBtn.grid(row=20, column=2)
        BackButton = ttk.Button(self, text="Back To HomePage", width=40,
                                command=lambda: controller.show_frame(MainPage))
        BackButton.grid(row=21, column=2)
        BackButton.grid_rowconfigure(5, weight=1)
        ActiveArea = Frame(self)
        ActiveArea.grid(row=4, column=2, sticky=W)
        ActiveArea.grid_rowconfigure(5, weight=1)

        self.ResultTreeview = Treeview(ActiveArea, columns=["ISBN", "Book Title", "Author(s)", "Availability"])
        self.ResultTreeview.grid(row=5, column=2)
        self.ResultTreeview.grid_rowconfigure(5, weight=1)
        self.ResultTreeview.heading('#0', text="ISBN")
        self.ResultTreeview.heading('#1', text="Book Title")
        self.ResultTreeview.heading('#2', text="Author(s)")
        self.ResultTreeview.heading('#3', text="Availability")
        self.ResultTreeview.bind('<ButtonRelease-1>', self.CheckoutBook)

    def CheckoutBook(self, a):
        curItem = self.ResultTreeview.focus()
        # self.bookIsbn = self.ResultTreeview.item(curItem)['text']
        self.bookIsbn = self.ResultTreeview.item(curItem)['text']

    def BookCheckOut(self):
        today = date.today()
        # today = datetime(2022, 10, 30)
        # print(self.bookIsbn)
        if self.bookIsbn is None:
            GenerateMessage("Attention! , Select Book First!")
            return None
        self.borrowerId = simpledialog.askstring("Check Out Book", "Enter Borrower ID")
        cursor = LibraryDB.cursor()
        cursor.execute(
            "SELECT EXISTS(SELECT CardID from BORROWERS WHERE CardID = '" + str(self.borrowerId) + "')")
        result = cursor.fetchall()

        if result == [(0,)]:
            GenerateMessage("Error! , Borrower not in Database!")
            return None
        else:
            count = 0
            cursor = LibraryDB.cursor()
            cursor.execute(
                "SELECT BOOK_LOANS.Date_in from BOOK_LOANS WHERE BOOK_LOANS.Card_id = '" + str(self.borrowerId) + "'")
            result = cursor.fetchall()
            for elem in result:
                if elem[0] is None:
                    count += 1
            if count >= 3:
                GenerateMessage("Not Allowed!, Borrower has loaned 3 books already!")
                return None
            else:
                cursor = LibraryDB.cursor()
                cursor.execute("SET FOREIGN_KEY_CHECKS=0")
                cursor.execute(
                    "INSERT INTO BOOK_LOANS (ISBN, Card_id, Date_out, Due_date) VALUES ('" + self.bookIsbn + "', '" + self.borrowerId + "', '" + str(
                        today) + "', '" + str(today + timedelta(days=14)) + "')")
                cursor.execute("SET FOREIGN_KEY_CHECKS=1")
                LibraryDB.commit()
                cursor = LibraryDB.cursor()
                cursor.execute("SELECT MAX(Loan_Id) FROM BOOK_LOANS")
                result = cursor.fetchall()
                loan_id = result[0][0]
                cursor.execute(
                    "INSERT INTO FINES (Loan_Id, fine_amt, paid) VALUES ('" + str(loan_id) + "', '0.00', '0')")
                LibraryDB.commit()
                GenerateMessage("Done, Book Loaned Out!")

    def SearchBook(self, SearchTextBox):
        search_string = SearchTextBox.get()
        # print("Search operation keyword : ")
        # print(search_string)
        # if LibraryDB.is_connected():
        #     print("Db conected, Searching book")
        cursor = LibraryDB.cursor()
        search_item = "'%" + str(search_string) + "%'"
        # print(search_item)
        cursor.execute("select book.isbn, BOOK.title, group_concat(AUTHORS.name) from BOOK join BOOK_AUTHORS on "
                       "BOOK.isbn = BOOK_AUTHORS.isbn "
                       "join AUTHORS on  BOOK_AUTHORS.author_id = AUTHORS.author_id where BOOK.title like" + search_item + "or AUTHORS.name like " + search_item + "or BOOK.isbn like " + search_item + "group by BOOK_AUTHORS.isbn")


        # cursor.execute("SELECT isbn,title from book where title like " + search_item)
        data = cursor.fetchall()
        # print("Search complete")
        self.view_data(data)

    def view_data(self, data):
        """
        View data on Treeview method.
        """
        self.ResultTreeview.delete(*self.ResultTreeview.get_children())

        for elem in data:
            cursor = LibraryDB.cursor()
            # print(str(elem[0]))
            # print(str(elem[1]))
            # print(str(elem[2]))
            cursor.execute(
                "SELECT EXISTS(SELECT BOOK_LOANS.isbn from BOOK_LOANS where BOOK_LOANS.isbn = '" + str(elem[0]) + "')")
            result = cursor.fetchall()
            # print(str(result))
            if str(result) == '[(0,)]':
                availability = "Available"
                # print(availability)
            else:
                cursor = LibraryDB.cursor()
                cursor.execute(
                    "SELECT BOOK_LOANS.Date_in from BOOK_LOANS where BOOK_LOANS.isbn = '" + str(elem[0]) + "'")
                result = cursor.fetchall()
                # print(result)
                if result[-1][0] is None:
                    availability = "Not Available"
                else:
                    availability = "Available"
            self.ResultTreeview.insert('', 'end', text=str(elem[0]), values=(str(elem[1]), str(elem[2]), availability))


def update_fine():
    todays_date = date.today()
    cursor = LibraryDB.cursor()
    cursor.execute("SELECT BOOK_LOANS.Loan_Id, BOOK_LOANS.Date_in, BOOK_LOANS.Due_date FROM BOOK_LOANS")
    result = cursor.fetchall()
    for record in result:
        date_in = record[1]
        date_due = record[2]
        if date_in is None:
            date_in = todays_date
        diff = (date_in - date_due)
        if diff.days > 0:
            fine = int(diff.days) * 0.25
        else:
            fine = 0
        cursor = LibraryDB.cursor()
        cursor.execute(
            "UPDATE FINES SET FINES.fine_amt = '" + str(fine) + "' WHERE FINES.Loan_Id = '" + str(record[0]) + "'")
        LibraryDB.commit()
        # cursor.execute("SELECT * FROM FINES")
        # records = cursor.fetchall()
        # for r in records:
        #     print(r)


class PayFines(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.v = StringVar()
        ttk.Label(self, text="Enter Borrower ID").grid(row=0, column=0, padx=20, pady=20)
        borrowerEntry = ttk.Entry(self)
        borrowerEntry.grid(row=1, column=2, padx=20, pady=20)
        showfinesbtn = ttk.Button(self, text="Show Fines", command=lambda: self.show_fines(borrowerEntry))
        showfinesbtn.grid(row=2, column=2, padx=20, pady=20)
        fineLabel = ttk.Label(self, textvariable=self.v)
        fineLabel.grid(row=3, column=2, padx=20, pady=20)
        payfinesbtn = ttk.Button(self, text="Pay Fine", command=lambda: self.pay_fine(borrowerEntry))
        payfinesbtn.grid(row=4, column=2, padx=20, pady=20)
        BackButton = ttk.Button(self, text="Back To HomePage", width=40,
                                command=lambda: controller.show_frame(MainPage))
        BackButton.grid(row=20, column=2)
        BackButton.grid_rowconfigure(5, weight=1)

    def pay_fine(self, borrowerEntry):
        borrower_id = borrowerEntry.get()
        cursor = LibraryDB.cursor()
        cursor.execute(
            "SELECT EXISTS(SELECT CardID FROM BORROWERS WHERE BORROWERS.CardID = '" + str(borrower_id) + "')")
        result = cursor.fetchall()
        if result == [(0,)]:
            GenerateMessage("Error Borrower does not exist!!")
        else:
            cursor = LibraryDB.cursor()
            cursor.execute(
                "SELECT FINES.Loan_Id FROM FINES JOIN BOOK_LOANS ON FINES.Loan_Id = BOOK_LOANS.Loan_Id WHERE "
                "BOOK_LOANS.Card_id = '" + str(
                    borrower_id) + "'")
            result = cursor.fetchall()
            for elem in result:
                cursor = LibraryDB.cursor()
                cursor.execute("UPDATE FINES SET FINES.paid = 1 WHERE FINES.Loan_Id = '" + str(elem[0]) + "'")
                LibraryDB.commit()
            GenerateMessage("Fines Paid Successfully!")

    def show_fines(self, borrowerEntry):
        total_fine = 0
        borrower_id = borrowerEntry.get()
        update_fine()
        # print("BorrowerID = " + str(borrower_id))
        cursor = LibraryDB.cursor()
        cursor.execute(
            "SELECT EXISTS(SELECT CardID FROM BORROWERS WHERE BORROWERS.CardID = '" + str(borrower_id) + "')")
        result = cursor.fetchall()
        # print(result)
        if result == [(0,)]:
            GenerateMessage("Error,Borrower does not exist!!")
            # print("Empty")
        else:
            cursor.execute(
                "SELECT FINES.fine_amt, FINES.paid FROM FINES JOIN BOOK_LOANS ON FINES.Loan_Id = BOOK_LOANS.Loan_Id "
                "WHERE BOOK_LOANS.Card_id = '" + str(
                    borrower_id) + "'")
            result = cursor.fetchall()
            total_fine = 0
            for elem in result:
                if elem[1] == 0:
                    total_fine += float(elem[0])

        self.v.set("Fine: $ " + str(total_fine))


LibraryUI()
mainloop()
