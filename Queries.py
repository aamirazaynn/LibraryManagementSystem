import pyodbc
import User

# Connection
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-57F9CL8'
BATABASE_NAME = 'LibraryManagementSystem'
connection = pyodbc.connect(
    f'DRIVER={DRIVER_NAME};SERVER={SERVER_NAME};DATABASE={BATABASE_NAME}; Trusted_Connection=yes;'
)


def deleteAllTablesContent(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Borrow;")
    cursor.execute("DELETE FROM [User];")
    cursor.execute("DELETE FROM Write;")
    cursor.execute("DELETE FROM Category;")
    cursor.execute("DELETE FROM Copy;")
    cursor.execute("DELETE FROM Book;")
    cursor.execute("DELETE FROM Author;")
    connection.commit()
    #read(connection)

def checkIfCategoryExists(CategoryName):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Category WHERE CategoryName = '{CategoryName}'")
    list = cursor.fetchall()
    check = False

    for row in list:
        cName = row[1]
        if(cName == CategoryName):
            check = (cName == CategoryName)
    connection.commit()        
    return check

def creatNewCategory(CategoryName):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Category")
    list = cursor.fetchall()
    cID = 1
    for row in list:
        cID += 1
    insertIntoCategory(cID, CategoryName)
    connection.commit()

def checkIfAuthorExists(AuthorName):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Author WHERE name = '{AuthorName}'")
    list = cursor.fetchall()
    check = False

    for row in list:
        aName = row[1]
        if(aName == AuthorName):
            check = (aName == AuthorName)
    connection.commit()
    return check

def checkIfBookExists(ISBN):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Book WHERE ISBN = '{ISBN}'")
    list = cursor.fetchall()
    check = False

    for row in list:
        isbn = row[2]
        if(isbn == ISBN):
            check = True
    connection.commit()
    return check

def creatNewAuthor(AuthorName):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Author")
    list = cursor.fetchall()
    aID = 1
    for row in list:
        aID += 1
    insertIntoAuthor(aID, AuthorName)
    connection.commit()
    
def getCategoryID(CategoryName):
    cursor = connection.cursor()
    cursor.execute(f"SELECT categoryID FROM Category WHERE CategoryName = '{CategoryName}'")
    list = cursor.fetchall()
    cID = list[0][0]
    int(cID)
    connection.commit()
    return cID

def getAuthorID(AuthorName):
    cursor = connection.cursor()
    cursor.execute(f"SELECT authorID FROM Author WHERE name = '{AuthorName}'")
    list = cursor.fetchall()
    aID = list[0][0]
    int(aID)
    connection.commit()
    return aID

def isuniqueISBN(ISBN):
    cursor = connection.cursor()
    cursor.execute(f"SELECT ISBN FROM Book")
    list = cursor.fetchall()
    check = True
    for row in list:
        isbn = row[0]
        if(isbn == ISBN):
            check = False
    connection.commit()
    return check

def decreaseNumberOfCopies(ISBN):
    cursor = connection.cursor()
    cursor.execute(f"UPDATE Copy SET Number = Number - 1 WHERE ISBN = {ISBN}")
    connection.commit()

def getUniqueUserID():
    cursor = connection.cursor()
    cursor.execute(f"SELECT UserID FROM [User]")
    list = cursor.fetchall()
    uID = 1
    for row in list:
        uID += 1
    connection.commit()
    return uID
    
def isUniqueEmail(Email):
    cursor = connection.cursor()
    cursor.execute(f"SELECT Email FROM [User]")
    list = cursor.fetchall()
    check = True
    for row in list:
        email = row[0]
        if(email == Email):
            check = not (email == Email)
    connection.commit()
    return check

def checkIfUserExists(Email): 
    cursor = connection.cursor()
    cursor.execute(f"SELECT email FROM [User]")
    list = cursor.fetchall()
    check = False
    for row in list:
        email = row[0]
        if(email == Email):
            check = (email == Email)
    connection.commit()
    return check

def checkIfPasswordCorrect(Email, Password):
    cursor = connection.cursor()
    cursor.execute(f"SELECT email, password FROM [User]")
    list = cursor.fetchall()
    check = False
    for row in list:
        e = row[0]
        p = row[1]
        if(p == Password and e == Email):
            check = True
    connection.commit()
    return check

def getUserDetailsByEmail(email):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM [User] WHERE Email = '{email}'")
    users = cursor.fetchall()
    u = None
    for user in users:
        FirstName = user[0]
        LastName = user[1]
        ID = user[2]
        Email = user[3]
        Role = user[4]
        Password = user[5]
    
    u = User.User(FirstName, LastName, ID, Email, Role, Password)
    return u

def createUniqueBorrowID():
    cursor = connection.cursor()
    cursor.execute(f"SELECT BorrowID FROM Borrow")
    list = cursor.fetchall()
    bID = 1
    for row in list:
        bID += 1
    connection.commit()
    return bID

# get unique number to coby
def createUniqueNumber(ISBN):
    cursor = connection.cursor()
    cursor.execute(f"SELECT Number FROM Copy where ISBN = {ISBN} order by Number")
    list = cursor.fetchall()
    num = 1
    for row in list:
        num += 1
    connection.commit()
    return num

# check if there is an  available copy
def checkIfAvailableCopy(ISBN):
    cursor = connection.cursor()
    cursor.execute(f"SELECT Number FROM Copy where ISBN = {ISBN} and status = 'available' order by Number")
    list = cursor.fetchall()
    check = False
    for row in list:
        num = row[0]
        if(num > 0):
            check = True
    connection.commit()
    return check

# ------------------------------------------------------------------------- insert statements ------------------------------------------------------------------------

# Insert data in book table
def insertIntoBook(ISBN,title,publisherName,publicationYear,categoryId):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO Book (ISBN,title,publisherName,publicationYear,categoryId) VALUES ('{ISBN}', '{title}', '{publisherName}', '{publicationYear}', {categoryId})")
    connection.commit()
    #read(connection)

# Insert data in Author table
def insertIntoAuthor(AuthorID,name):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO Author (AuthorID, name) VALUES ({AuthorID}, '{name}')")
    connection.commit()
    #read(connection)

# Insert data in Category table
def insertIntoCategory(CategoryID,CategoryName):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO Category (CategoryID, CategoryName) VALUES ({CategoryID}, '{CategoryName}')")
    connection.commit()
    #read(connection)

# Insert data in Borrow table
def insertIntoBorrow(ReturnDate,BorrowDate,BorrowID,ISBN,UserID, number):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO Borrow (ReturnDate,BorrowDate,BorrowID,ISBN,UserID,Number) VALUES ('{ReturnDate}','{BorrowDate}', {BorrowID}, {ISBN}, {UserID}, {number})")
    connection.commit()
    #read(connection)

# Insert data in Copy table
def insertIntoCopy(ISBN):
    Number = createUniqueNumber(ISBN)
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO Copy (Number, ISBN, Status) VALUES ({Number}, {ISBN}, 'available')")
    connection.commit()
    #read(connection)

# Insert data in Write table
def insertIntoWrite(ISBN, AuthorID):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO Write (ISBN, AuthorID) VALUES ({ISBN}, {AuthorID})")
    connection.commit()
    #read(connection)

# Insert data in User table
def insertIntoUser(FirstName,LastName,UserID,Email,Role,Password):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO [User] (FirstName, LastName, UserID, Email, Role, Password) VALUES ('{FirstName}', '{LastName}', {UserID}, '{Email}', '{Role}', '{Password}')")
    connection.commit()
    #read(connection)

# ------------------------------------------------------------------------- delete statements ------------------------------------------------------------------------

# Delete data from book table with condition
def deleteFromBook(ISBN):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM Book WHERE ISBN ={ISBN};")
    connection.commit()

# Delete data from Author table with condition
def deleteFromAuthor(AuthorID):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM Author WHERE AuthorID ={AuthorID};")
    connection.commit()
    #read(connection)

# Delete data from Category table with condition
def deleteFromCategory(CategoryID):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM Category WHERE CategoryID ={CategoryID};")
    connection.commit()
    #read(connection)

# Delete data from Borrow table with condition
def deleteFromBorrow(BorrowID):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM Borrow WHERE BorrowID ={BorrowID};")
    connection.commit()
    #read(connection)

def deleteFromCopyByISBN(ISBN):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM Copy WHERE ISBN ={ISBN};")
    connection.commit()

# Delete data from Write table with condition
def deleteFromWrite(ISBN):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM Write WHERE ISBN ={ISBN};")
    connection.commit()
    #read(connection)

# Delete data from User table with condition
def deleteFromUser(UserID):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM [User] WHERE UserID ={UserID};")
    connection.commit()
    #read(connection)

# ------------------------------------------------------------------------- update statements ------------------------------------------------------------------------

# Update data in book table
def updateBook(ISBN,title,publisherName,publicationYear,categoryId):
    cursor = connection.cursor()
    cursor.execute(f"UPDATE Book SET Title = '{title}', PublisherName = '{publisherName}', PublicationYear = {publicationYear}, CategoryId = {categoryId} WHERE ISBN = {ISBN}")
    connection.commit()
    #read(connection)

# Update data in User table
def updateUser(FirstName,LastName,UserID,Email,Password):
    cursor = connection.cursor()
    cursor.execute(f"UPDATE [User] SET FirstName = '{FirstName}', LastName = '{LastName}', Email = '{Email}', Password = '{Password}' WHERE UserID = {UserID}")
    connection.commit()

# update data in copy table
def updateCopy(Number,ISBN):
    deleteFromCopyByISBN(ISBN)
    while Number != 0:
        insertIntoCopy(ISBN)
        Number = Number - 1

# update aviailablity copy
def updateAvailableCopyByISBN(Number, ISBN):
    cursor = connection.cursor()
    cursor.execute(f"UPDATE Copy SET Status = 'inavailable' WHERE ISBN = {ISBN} and Number = {Number}")
    connection.commit()

# ------------------------------------------------------------ Select data from any table(s) of the database ---------------------------------------------------------

# Select all books
def selectAllFromBook():
    cursor = connection.cursor()
    cursor.execute("SELECT ISBN, title, publisherName, publicationYear FROM Book")
    books = cursor.fetchall()
    return books

# Select all categories
def selectAllFromCategory():
    cursor = connection.cursor()
    cursor.execute("SELECT CategoryID, CategoryName FROM Category")
    Categories = cursor.fetchall()
    
    for book in Categories:
        CategoryID = book[0]
        CategoryName = book[1]

# Select book by its title
def selectBookByTitle(title):
    cursor = connection.cursor()
    cursor.execute(f"SELECT ISBN, title, publisherName, publicationYear FROM Book WHERE title like '{title}%'")
    books = cursor.fetchall()
    
# Select User Info by his/her UserID
def selectUserByUserID(UserID):
    cursor = connection.cursor()
    cursor.execute(f"SELECT FirstName, LastName, Email, Password FROM [User] WHERE UserID = {UserID}")
    users = cursor.fetchall()
    
    for user in users:
        FirstName = user[0]
        LastName = user[1]
        Email = user[2]
        Password = user[3]
        
def selectAllBookAuthors():
    cursor = connection.cursor()
    cursor.execute(f"select a.name from author a, book b, write w where b.ISBN = w.ISBN and a.authorID = w.authorID")
    authors = cursor.fetchall()

    return authors

# get available copy by ISBN
def selectAvailableCopyByISBN(ISBN):
    cursor = connection.cursor()
    cursor.execute(f"SELECT Number FROM Copy WHERE ISBN = {ISBN} and Status = 'available'")
    list = cursor.fetchall()
    Number = list[0][0]
    return Number

# ----------------------------------------------- Select data that involves more than one table of the database (using joins) ----------------------------------------

# Select books from spesific category
def selectBookByCategoryName(CategoryName):
    cursor = connection.cursor()
    cursor.execute(f"SELECT ISBN, title, publisherName, publicationYear, CategoryName FROM Book as b left join Category as c on b.CategoryID = c.CategoryID where c.CategoryName = '{CategoryName}'")
    books = cursor.fetchall()

# Select book by its Author
def selectBookByAuthor(AuthorName):
    cursor = connection.cursor()
    cursor.execute(f"SELECT b.ISBN, b.title, a.Name FROM Book AS b JOIN Write AS w ON b.ISBN = w.ISBN JOIN Author AS a ON w.AuthorID = a.AuthorID WHERE a.Name LIKE '{AuthorName}%'")
    books = cursor.fetchall()

def selectAllBooksCategories():
    cursor = connection.cursor()
    cursor.execute(f"select categoryName From Book as b left join Category as c on c.CategoryID = b.CategoryID")
    categories = cursor.fetchall()

    return categories

# ----------------------------------------------------------------------------search statements ------------------------------------------------------------------------

def searchByAuthor(AuthorName):
    cursor = connection.cursor()
    cursor.execute(f"select b.ISBN, Title, Name, PublisherName, PublicationYear, CategoryName from Book b, Author a, Category c, Write w where b.ISBN in (select ISBN from Author a , Write W  where a.AuthorID = w.AuthorID and name like '%{AuthorName}%') and name in (select Name from Author a , Write W where a.AuthorID = w.AuthorID and name like '%{AuthorName}%') and b.CategoryID = c.CategoryID and a.AuthorID = w.AuthorID and b.ISBN = w.ISBN")
    return cursor.fetchall()

def searchByISBN(ISBN):
    cursor = connection.cursor()
    cursor.execute(f"select b.ISBN, Title, Name, PublisherName, PublicationYear, CategoryName from Book b, Author a, Category c, Write w where b.ISBN in (select ISBN from Author a , Write W  where a.AuthorID = w.AuthorID) and name in (select Name from Author a , Write W where a.AuthorID = w.AuthorID) and b.CategoryID = c.CategoryID and a.AuthorID = w.AuthorID and b.ISBN = w.ISBN and b.isbn = {ISBN}")
    return cursor.fetchall()

def searchByYear(Year):
    cursor = connection.cursor()
    cursor.execute(f"select b.ISBN, Title, Name, PublisherName, PublicationYear, CategoryName from Book b, Author a, Category c, Write w where b.ISBN in (select ISBN from Author a , Write W  where a.AuthorID = w.AuthorID) and name in (select Name from Author a , Write W where a.AuthorID = w.AuthorID) and b.CategoryID = c.CategoryID and a.AuthorID = w.AuthorID and b.ISBN = w.ISBN and b.PublicationYear = {Year}")
    return cursor.fetchall()

def searchByTitle(Title):
    cursor = connection.cursor()
    cursor.execute(f"select b.ISBN, Title, Name, PublisherName, PublicationYear, CategoryName from Book b, Author a, Category c, Write w where b.ISBN in (select ISBN from Author a , Write W  where a.AuthorID = w.AuthorID) and name in (select Name from Author a , Write W where a.AuthorID = w.AuthorID) and b.CategoryID = c.CategoryID and a.AuthorID = w.AuthorID and b.ISBN = w.ISBN and b.Title like '%{Title}%'")
    return cursor.fetchall()